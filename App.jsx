import { motion } from 'framer-motion';
import { CommandLineIcon, UserGroupIcon, CogIcon, ChatBubbleBottomCenterTextIcon, ShieldCheckIcon, EyeIcon, MoonIcon, UserIcon, UserMinusIcon, UserPlusIcon } from '@heroicons/react/24/outline';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 text-white">
      {/* Hero Section */}
      <header className="container mx-auto px-4 py-24 text-center relative overflow-hidden">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative z-10"
        >
          <h1 className="text-7xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-500">
            Werewolf Bot
          </h1>
          <p className="text-2xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Discordサーバーで簡単に人狼ゲームを楽しめる、全自動進行の次世代ボット
          </p>
          <div className="flex justify-center gap-4">
            <a
              href="https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot%20applications.commands"
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-8 rounded-full text-lg transition-all transform hover:scale-105 hover:shadow-lg"
            >
              ボットを招待する
            </a>
            <a
              href="#features"
              className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-4 px-8 rounded-full text-lg transition-all transform hover:scale-105"
            >
              機能を見る
            </a>
          </div>
        </motion.div>
        <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 blur-3xl"></div>
      </header>

      {/* Features */}
      <section id="features" className="py-24 bg-gray-800/50">
        <div className="container mx-auto px-4">
          <h2 className="text-5xl font-bold text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-500">
            主な機能
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <Feature
              icon={<CommandLineIcon className="h-12 w-12" />}
              title="簡単セットアップ"
              description="スラッシュコマンドで直感的な操作。セットアップから開始まで1分以内"
            />
            <Feature
              icon={<UserGroupIcon className="h-12 w-12" />}
              title="柔軟な人数設定"
              description="4〜20人まで対応。人数に応じて役職を最適に自動配分"
            />
            <Feature
              icon={<CogIcon className="h-12 w-12" />}
              title="全自動進行"
              description="投票システムや役職の行動をボットが完全自動化"
            />
            <Feature
              icon={<ChatBubbleBottomCenterTextIcon className="h-12 w-12" />}
              title="リアルタイム通知"
              description="DMで役職や行動結果を即時通知。ゲーム状況を完全把握"
            />
          </div>
        </div>
      </section>

      {/* Roles */}
      <section className="py-24">
        <div className="container mx-auto px-4">
          <h2 className="text-5xl font-bold text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-500">
            役職紹介
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <Role
              icon={<UserIcon />}
              title="村人"
              team="村人陣営"
              description="投票で人狼を見つけ出し、村を守る一般市民。正しい推理が勝利の鍵"
            />
            <Role
              icon={<MoonIcon />}
              title="人狼"
              team="人狼陣営"
              description="夜に村人を襲撃する。仲間と協力して村人を欺き、数を減らすのが目的"
            />
            <Role
              icon={<EyeIcon />}
              title="占い師"
              team="村人陣営"
              description="毎夜、一人を占って人狼かどうかを知ることができる特殊能力者"
            />
            <Role
              icon={<ShieldCheckIcon />}
              title="狩人"
              team="村人陣営"
              description="毎夜、一人を人狼の襲撃から守ることができる村の守護者"
            />
            <Role
              icon={<UserMinusIcon />}
              title="霊媒師"
              team="村人陣営"
              description="処刑された人物が人狼だったかどうかを知ることができる特殊能力者"
            />
            <Role
              icon={<UserPlusIcon />}
              title="共犯者"
              team="人狼陣営"
              description="人狼の協力者。人狼のふりをして村人を混乱させるスパイ"
            />
          </div>
        </div>
      </section>

      {/* Game Flow */}
      <section className="py-24 bg-gray-800/50">
        <div className="container mx-auto px-4">
          <h2 className="text-5xl font-bold text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-500">
            ゲームの流れ
          </h2>
          <div className="max-w-4xl mx-auto space-y-12">
            <GamePhase
              number="1"
              title="準備フェーズ"
              description="ボットがチャンネルを作成し、参加者を募集。設定完了後、全員に役職をDMで通知"
            />
            <GamePhase
              number="2"
              title="昼フェーズ"
              description="全員で議論を行い、怪しい人物を推理。設定された時間が経過すると投票フェーズへ"
            />
            <GamePhase
              number="3"
              title="投票フェーズ"
              description="全員で投票を実施。最多票を得たプレイヤーが処刑されます"
            />
            <GamePhase
              number="4"
              title="夜フェーズ"
              description="人狼による襲撃、占い師の占い、狩人の護衛など、各役職が行動を実行"
            />
          </div>
        </div>
      </section>

      {/* Commands */}
      <section className="py-24">
        <div className="container mx-auto px-4">
          <h2 className="text-5xl font-bold text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-500">
            主なコマンド
          </h2>
          <div className="max-w-3xl mx-auto space-y-6">
            <Command
              name="/werewolf"
              description="新しい人狼ゲームを作成します"
            />
            <Command
              name="/start"
              description="参加者が揃ったらゲームを開始します"
            />
            <Command
              name="/end"
              description="進行中のゲームを終了します"
            />
            <Command
              name="/kick @ユーザー名"
              description="指定したプレイヤーをゲームから除外します"
            />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 py-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">© 2023 Werewolf Bot. All rights reserved.</p>
          <div className="mt-4 space-x-4">
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              プライバシーポリシー
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              利用規約
            </a>
            <a href="#" className="text-gray-400 hover:text-white transition-colors">
              お問い合わせ
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

function Feature({ icon, title, description }) {
  return (
    <motion.div
      className="p-8 bg-gray-700/50 rounded-xl backdrop-blur-sm border border-gray-700"
      whileHover={{ scale: 1.05 }}
      transition={{ type: "spring", stiffness: 300 }}
    >
      <div className="text-indigo-400 mb-4">{icon}</div>
      <h3 className="text-xl font-bold mb-2">{title}</h3>
      <p className="text-gray-300">{description}</p>
    </motion.div>
  );
}

function Role({ icon, title, team, description }) {
  return (
    <motion.div
      className="p-6 bg-gray-800 rounded-xl border border-gray-700"
      whileHover={{ scale: 1.02 }}
      transition={{ type: "spring", stiffness: 300 }}
    >
      <div className="text-indigo-400 mb-4 h-8 w-8">{icon}</div>
      <h3 className="text-xl font-bold mb-1">{title}</h3>
      <p className="text-sm text-indigo-400 mb-2">{team}</p>
      <p className="text-gray-300 text-sm">{description}</p>
    </motion.div>
  );
}

function GamePhase({ number, title, description }) {
  return (
    <motion.div
      className="flex items-start gap-6 p-6 bg-gray-700/30 rounded-xl backdrop-blur-sm"
      initial={{ opacity: 0, x: -20 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex-shrink-0 w-12 h-12 bg-indigo-600 rounded-full flex items-center justify-center text-xl font-bold">
        {number}
      </div>
      <div>
        <h3 className="text-2xl font-bold mb-2">{title}</h3>
        <p className="text-gray-300">{description}</p>
      </div>
    </motion.div>
  );
}

function Command({ name, description }) {
  return (
    <motion.div
      className="p-4 bg-gray-800/50 rounded-lg border border-gray-700 flex items-center"
      whileHover={{ scale: 1.01 }}
      transition={{ type: "spring", stiffness: 300 }}
    >
      <code className="text-indigo-400 font-mono mr-4">{name}</code>
      <p className="text-gray-300">{description}</p>
    </motion.div>
  );
}

export default App;