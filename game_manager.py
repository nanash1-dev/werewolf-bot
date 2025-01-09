from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Set, Optional, Tuple
import random

class GamePhase(Enum):
    WAITING = "waiting"
    DAY = "day"
    VOTE = "vote"
    NIGHT = "night"
    FINISHED = "finished"

class Role(Enum):
    WEREWOLF = "人狼"
    VILLAGER = "村人"
    GUARD = "狩人"
    SEER = "占い師"
    MEDIUM = "霊媒師"
    ACCOMPLICE = "共犯者"

@dataclass
class PlayerState:
    member_id: int
    role: Optional[Role] = None
    is_alive: bool = True
    is_protected: bool = False
    last_action_target: Optional[int] = None
    last_action_day: int = 0
    vote_cast: bool = False
    action_performed: bool = False

class GameState:
    def __init__(self, creator_id: int, channel_id: int):
        self.creator_id = creator_id
        self.channel_id = channel_id
        self.text_channel_id: Optional[int] = None
        self.voice_channel_id: Optional[int] = None
        self.phase = GamePhase.WAITING
        self.players: Dict[int, PlayerState] = {}
        self.max_players = 20
        self.min_players = 4
        self.banned_players: Set[int] = set()
        self.allowed_players: Set[int] = set()
        self.dm_invites: Set[int] = set()
        self.vote_time_minutes = 5
        self.game_name = ""
        self.day = 1
        self.votes: Dict[int, int] = {}
        self.night_actions: Dict[int, int] = {}
        self.action_logs: List[str] = []
        self.last_eliminated: Optional[int] = None
        self.last_killed: Optional[int] = None
        self.recruitment_end_time: Optional[datetime] = None
        self.started_at: Optional[datetime] = None
        self.phase_end_time: Optional[datetime] = None

    def calculate_roles(self) -> bool:
        """役職を計算して割り当てる"""
        if len(self.players) < self.min_players:
            return False

        player_ids = list(self.players.keys())
        random.shuffle(player_ids)
        
        # プレイヤー数に応じた役職の割り当て
        total_players = len(player_ids)
        role_counts = self._calculate_role_distribution(total_players)

        # 役職の割り当て
        current_index = 0
        for role, count in role_counts.items():
            for _ in range(count):
                if current_index < len(player_ids):
                    player_id = player_ids[current_index]
                    self.players[player_id].role = role
                    current_index += 1

        # 残りのプレイヤーを村人に
        while current_index < len(player_ids):
            player_id = player_ids[current_index]
            self.players[player_id].role = Role.VILLAGER
            current_index += 1

        return True

    def _calculate_role_distribution(self, total_players: int) -> Dict[Role, int]:
        """プレイヤー数に応じた役職の分布を計算"""
        role_counts = {
            Role.WEREWOLF: max(1, total_players // 4),
            Role.SEER: 1,
            Role.GUARD: 1 if total_players >= 6 else 0,
            Role.MEDIUM: 1 if total_players >= 8 else 0,
            Role.ACCOMPLICE: 1 if total_players >= 10 else 0
        }
        return role_counts

    def get_alive_players(self) -> List[int]:
        """生存しているプレイヤーのIDリストを取得"""
        return [pid for pid, state in self.players.items() if state.is_alive]

    def get_players_by_role(self, role: Role) -> List[int]:
        """指定された役職の生存プレイヤーのIDリストを取得"""
        return [pid for pid, state in self.players.items() 
                if state.role == role and state.is_alive]

    def is_game_over(self) -> Tuple[bool, Optional[str]]:
        """ゲーム終了条件をチェック"""
        werewolf_count = len([p for p in self.players.values() 
                            if p.is_alive and p.role in [Role.WEREWOLF, Role.ACCOMPLICE]])
        villager_count = len([p for p in self.players.values() 
                            if p.is_alive and p.role not in [Role.WEREWOLF, Role.ACCOMPLICE]])

        if werewolf_count == 0:
            return True, "村人陣営"
        elif werewolf_count >= villager_count:
            return True, "人狼陣営"
        return False, None

    def add_log(self, message: str):
        """ゲームログにメッセージを追加"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.action_logs.append(f"[{timestamp}] {message}")

    def handle_night_actions(self) -> Tuple[Optional[int], List[Tuple[str, int, Optional[int], Optional[Role]]]]:
        """夜のアクションを処理"""
        messages = []
        killed_player = None
        
        # 占い師のアクション
        for seer_id in self.get_players_by_role(Role.SEER):
            if seer_id in self.night_actions:
                target_id = self.night_actions[seer_id]
                target_role = self.players[target_id].role
                messages.append(("seer", seer_id, target_id, target_role))
                self.players[seer_id].last_action_target = target_id
                self.players[seer_id].last_action_day = self.day

        # 狩人のアクション
        for guard_id in self.get_players_by_role(Role.GUARD):
            if guard_id in self.night_actions:
                target_id = self.night_actions[guard_id]
                # 同じ対象を連続で守れない
                if self.players[guard_id].last_action_target != target_id:
                    self.players[target_id].is_protected = True
                    self.players[guard_id].last_action_target = target_id
                    self.players[guard_id].last_action_day = self.day
                    messages.append(("guard", guard_id, target_id, None))

        # 人狼のアクション
        werewolf_votes = {}
        for werewolf_id in self.get_players_by_role(Role.WEREWOLF):
            if werewolf_id in self.night_actions:
                target_id = self.night_actions[werewolf_id]
                werewolf_votes[target_id] = werewolf_votes.get(target_id, 0) + 1

        if werewolf_votes:
            target_id = max(werewolf_votes.items(), key=lambda x: x[1])[0]
            if not self.players[target_id].is_protected:
                self.players[target_id].is_alive = False
                killed_player = target_id
                self.last_killed = target_id
                messages.append(("kill", target_id, None, None))
            else:
                messages.append(("protected", target_id, None, None))

        # 霊媒師のアクション
        if self.last_eliminated:
            for medium_id in self.get_players_by_role(Role.MEDIUM):
                eliminated_role = self.players[self.last_eliminated].role
                messages.append(("medium", medium_id, self.last_eliminated, eliminated_role))

        # 保護状態をリセット
        for player in self.players.values():
            player.is_protected = False

        return killed_player, messages

    def handle_voting(self) -> Optional[int]:
        """投票を処理して結果を返す"""
        if not self.votes:
            return None

        vote_counts = {}
        for target_id in self.votes.values():
            vote_counts[target_id] = vote_counts.get(target_id, 0) + 1

        # 最多得票者を特定
        max_votes = max(vote_counts.values())
        top_voted = [pid for pid, count in vote_counts.items() if count == max_votes]

        if len(top_voted) == 1:
            eliminated_id = top_voted[0]
            self.players[eliminated_id].is_alive = False
            self.last_eliminated = eliminated_id
            self.add_log(f"プレイヤー <@{eliminated_id}> が投票により処刑されました")
            return eliminated_id

        return None

    def reset_votes(self):
        """投票をリセット"""
        self.votes.clear()
        for player in self.players.values():
            player.vote_cast = False

    def reset_night_actions(self):
        """夜のアクションをリセット"""
        self.night_actions.clear()
        for player in self.players.values():
            player.action_performed = False

    def can_player_join(self, player_id: int) -> bool:
        """プレイヤーが参加可能かチェック"""
        if player_id in self.banned_players:
            return False
        if self.allowed_players and player_id not in self.allowed_players:
            return False
        if len(self.players) >= self.max_players:
            return False
        return True

    def is_ready_to_start(self) -> bool:
        """ゲーム開始可能かチェック"""
        return (
            len(self.players) >= self.min_players and
            len(self.players) <= self.max_players
        )