from typing import Dict, List, Optional
import discord
from discord import Embed, Color
from game_manager import GameState, Role, GamePhase

class MessageManager:
    @staticmethod
    def create_game_settings_embed() -> Embed:
        embed = Embed(
            title="人狼ゲーム設定",
            description="下のボタンから設定を変更できます",
            color=Color.blue()
        )
        embed.add_field(
            name="設定可能な項目",
            value=(
                "🎮 参加人数設定 (4-20人)\n"
                "🚫 参加規制設定\n"
                "📝 ゲーム名変更\n"
                "⏰ 投票時間設定 (1-10分)\n"
                "👥 参加可能ユーザー設定\n"
                "📨 DM招待設定"
            ),
            inline=False
        )
        embed.add_field(
            name="ゲーム開始条件",
            value=(
                "✅ 最低4人以上の参加者\n"
                "✅ 設定された参加人数の達成\n"
                "✅ ゲーム作成者による開始コマンド"
            ),
            inline=False
        )
        return embed

    @staticmethod
    def create_role_embed(player_id: int, game_state: GameState) -> Embed:
        player = game_state.players[player_id]
        role = player.role
        
        role_colors = {
            Role.WEREWOLF: Color.dark_red(),
            Role.VILLAGER: Color.green(),
            Role.GUARD: Color.blue(),
            Role.MEDIUM: Color.purple(),
            Role.SEER: Color.gold(),
            Role.ACCOMPLICE: Color.dark_red()
        }
        
        embed = Embed(
            title="あなたの役職",
            description=f"あなたは **{role.value}** です",
            color=role_colors.get(role, Color.default())
        )

        role_descriptions = {
            Role.WEREWOLF: (
                "🐺 人狼の役割:\n"
                "- 夜に村人を襲撃できます\n"
                "- 他の人狼と協力して村人を倒しましょう\n"
                "- 昼間は村人のふりをして疑いをかわしましょう"
            ),
            Role.VILLAGER: (
                "👥 村人の役割:\n"
                "- 投票で人狼を見つけ出し、処刑しましょう\n"
                "- 他の村人と協力して推理を進めましょう\n"
                "- 特殊能力は持っていませんが、投票が重要です"
            ),
            Role.GUARD: (
                "🛡️ 狩人の役割:\n"
                "- 夜に一人を人狼の襲撃から守ることができます\n"
                "- 守る対象は毎晩変える必要があります\n"
                "- 自分自身は守れません"
            ),
            Role.MEDIUM: (
                "👻 霊媒師の役割:\n"
                "- 処刑された人が人狼だったかどうかを知ることができます\n"
                "- この情報を活用して村人たちを導きましょう\n"
                "- ただし、情報の出し方には注意が必要です"
            ),
            Role.SEER: (
                "🔮 占い師の役割:\n"
                "- 夜に一人を占い、人狼かどうかを知ることができます\n"
                "- 得られた情報を村人たちと共有しましょう\n"
                "- ただし、早めに正体がばれると危険です"
            ),
            Role.ACCOMPLICE: (
                "🎭 共犯者の役割:\n"
                "- 人狼陣営の協力者です\n"
                "- 人狼のふりをして村人を混乱させましょう\n"
                "- 人狼を守りつつ、村人たちの信頼を得ましょう"
            )
        }

        embed.add_field(
            name="役割と注意点",
            value=role_descriptions[role],
            inline=False
        )

        if role in [Role.WEREWOLF, Role.ACCOMPLICE]:
            werewolves = [
                f"<@{pid}>" for pid in game_state.get_players_by_role(Role.WEREWOLF)
                if pid != player_id
            ]
            if werewolves:
                embed.add_field(
                    name="人狼のプレイヤー",
                    value="、".join(werewolves),
                    inline=False
                )

        embed.add_field(
            name="勝利条件",
            value=(
                "🏆 村人陣営: すべての人狼を処刑する\n"
                "🐺 人狼陣営: 村人の数を人狼と同じか少なくする"
            ),
            inline=False
        )

        return embed

    @staticmethod
    def create_game_status_embed(game_state: GameState) -> Embed:
        phase_colors = {
            GamePhase.DAY: Color.gold(),
            GamePhase.NIGHT: Color.dark_purple(),
            GamePhase.VOTE: Color.red(),
            GamePhase.FINISHED: Color.green()
        }

        phase_names = {
            GamePhase.DAY: "☀️ 昼",
            GamePhase.NIGHT: "🌙 夜",
            GamePhase.VOTE: "⚖️ 投票",
            GamePhase.FINISHED: "🏁 終了"
        }

        embed = Embed(
            title=f"ゲームステータス - {game_state.day}日目",
            color=phase_colors.get(game_state.phase, Color.blue())
        )

        # 生存者リスト
        alive_players = [
            f"<@{pid}>" 
            for pid in game_state.get_alive_players()
        ]
        embed.add_field(
            name="👥 生存者",
            value="\n".join(alive_players) if alive_players else "なし",
            inline=False
        )

        # フェーズ情報
        embed.add_field(
            name="📅 現在のフェーズ",
            value=phase_names.get(game_state.phase, "不明"),
            inline=False
        )

        # 追加情報
        if game_state.last_eliminated:
            embed.add_field(
                name="⚰️ 最後に処刑されたプレイヤー",
                value=f"<@{game_state.last_eliminated}>",
                inline=False
            )

        if game_state.last_killed:
            embed.add_field(
                name="💀 最後に襲撃されたプレイヤー",
                value=f"<@{game_state.last_killed}>",
                inline=False
            )

        return embed

    @staticmethod
    def create_voting_embed(game_state: GameState) -> Embed:
        embed = Embed(
            title="投票",
            description="処刑する人を選んでください",
            color=Color.red()
        )

        alive_players = game_state.get_alive_players()
        player_list = "\n".join(
            f"{i+1}. <@{pid}>" 
            for i, pid in enumerate(alive_players)
        )
        
        embed.add_field(
            name="投票可能なプレイヤー",
            value=player_list,
            inline=False
        )

        embed.add_field(
            name="投票方法",
            value=(
                "1️⃣ 番号のリアクションをクリックして投票\n"
                "⏰ 制限時間: 60秒\n"
                "❗ 投票は1回のみ可能です"
            ),
            inline=False
        )

        return embed

    @staticmethod
    def create_night_action_embed(player_id: int, game_state: GameState) -> Embed:
        player = game_state.players[player_id]
        role = player.role

        title_map = {
            Role.WEREWOLF: "🐺 襲撃する対象を選択",
            Role.SEER: "🔮 占う対象を選択",
            Role.GUARD: "🛡️ 守る対象を選択",
        }

        description_map = {
            Role.WEREWOLF: "今夜襲撃する村人を選んでください",
            Role.SEER: "占いをかける対象を選んでください",
            Role.GUARD: "今夜守る対象を選んでください",
        }

        embed = Embed(
            title=title_map.get(role, "アクション選択"),
            description=description_map.get(role, "行動を選択してください"),
            color=Color.dark_purple()
        )

        # 選択可能なプレイヤーリスト
        alive_players = [
            pid for pid in game_state.get_alive_players()
            if pid != player_id  # 自分以外
        ]
        player_list = "\n".join(f"{i+1}. <@{pid}>" for i, pid in enumerate(alive_players))
        
        embed.add_field(
            name="選択可能なプレイヤー",
            value=player_list,
            inline=False
        )

        # 役職ごとの注意事項
        notes_map = {
            Role.WEREWOLF: (
                "- 他の人狼と相談して決めましょう\n"
                "- 投票数が最も多い対象が襲撃されます\n"
                "- 狩人に守られている場合は襲撃が失敗します"
            ),
            Role.SEER: (
                "- 占った対象が人狼かどうかわかります\n"
                "- 結果はDMで通知されます\n"
                "- 情報の使い方は慎重に"
            ),
            Role.GUARD: (
                "- 同じ人を連続で守ることはできません\n"
                "- 自分自身は守れません\n"
                "- 守り先は秘密にしましょう"
            ),
        }

        if role in notes_map:
            embed.add_field(
                name="注意事項",
                value=notes_map[role],
                inline=False
            )

        return embed

    @staticmethod
    def create_game_result_embed(game_state: GameState, winner: str) -> Embed:
        embed = Embed(
            title="🏁 ゲーム終了",
            description=f"勝者: {winner}",
            color=Color.gold()
        )

        # 全プレイヤーの役職を表示
        role_list = []
        for player_id, player in game_state.players.items():
            status = "✅ 生存" if player.is_alive else "💀 死亡"
            role_list.append(f"<@{player_id}>: {player.role.value} ({status})")

        embed.add_field(
            name="📋 プレイヤーの役職",
            value="\n".join(role_list),
            inline=False
        )

        # 勝利条件の説明
        embed.add_field(
            name="🏆 勝利条件",
            value=(
                "村人陣営の勝利条件:\n"
                "- すべての人狼を処刑する\n\n"
                "人狼陣営の勝利条件:\n"
                "- 村人の数を人狼と同じか少なくする"
            ),
            inline=False
        )

        # ゲームログ
        if game_state.action_logs:
            log_text = "\n".join(game_state.action_logs[-10:])  # 最新の10件
            embed.add_field(
                name="📜 ゲームログ",
                value=log_text,
                inline=False
            )

        return embed