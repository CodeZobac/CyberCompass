import { BrutalNavigation } from '../../components/BrutalNavigation';
import { BrutalPageLayout } from '../../components/BrutalPageLayout';

export default function DeepfakeTrainingPage() {
  const breadcrumbs = [
    { label: 'Home', href: '/' },
    { label: 'AI Features', href: '/ai-features' },
    { label: 'Deepfake Training' }
  ];

  return (
    <>
      <BrutalNavigation />
      <BrutalPageLayout breadcrumbs={breadcrumbs}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          {/* Hero Section */}
          <section className="mb-16 text-center">
            <div className="inline-block mb-6">
              <div className="w-24 h-24 bg-brutal-red border-6 border-black shadow-brutal-lg flex items-center justify-center">
                <span className="text-6xl">🎭</span>
              </div>
            </div>
            <h1 className="text-5xl sm:text-7xl font-black uppercase mb-6 text-brutal-red">
              Deepfake Detection
              <br />
              Training
            </h1>
            <p className="text-xl sm:text-2xl font-bold text-brutal-gray-700 max-w-3xl mx-auto mb-8">
              Master the art of spotting manipulated media
            </p>

            {/* Stats Cards */}
            <div className="flex flex-wrap justify-center gap-4 mb-12">
              <div className="px-6 py-4 bg-white border-4 border-black shadow-brutal-md">
                <div className="text-3xl font-black text-brutal-blue">45</div>
                <div className="text-sm font-bold uppercase">Challenges</div>
              </div>
              <div className="px-6 py-4 bg-white border-4 border-black shadow-brutal-md">
                <div className="text-3xl font-black text-brutal-green">89%</div>
                <div className="text-sm font-bold uppercase">Accuracy</div>
              </div>
              <div className="px-6 py-4 bg-white border-4 border-black shadow-brutal-md">
                <div className="text-3xl font-black text-brutal-red">🔥 7</div>
                <div className="text-sm font-bold uppercase">Day Streak</div>
              </div>
            </div>

            <div className="flex flex-wrap justify-center gap-4">
              <button className="px-8 py-4 font-black uppercase text-lg border-6 border-black bg-brutal-red text-white shadow-brutal-lg hover-lift focus:outline-none focus:ring-4 focus:ring-brutal-red">
                Start Training →
              </button>
              <button className="px-8 py-4 font-black uppercase text-lg border-6 border-black bg-white hover:bg-brutal-gray-50 shadow-brutal-lg hover-lift focus:outline-none focus:ring-4 focus:ring-brutal-blue">
                View Progress
              </button>
            </div>
          </section>

          {/* Introduction Section */}
          <section className="mb-16 p-8 bg-brutal-gray-50 border-4 border-black">
            <h2 className="text-3xl font-black uppercase mb-4">What Are Deepfakes?</h2>
            <p className="text-lg font-semibold text-brutal-gray-700 mb-4">
              Deepfakes are synthetic media created using artificial intelligence to manipulate or generate visual and audio content. 
              They can make it appear as though someone said or did something they never actually did.
            </p>
            <p className="text-lg font-semibold text-brutal-gray-700">
              Learning to detect deepfakes is crucial in today&apos;s digital landscape where misinformation can spread rapidly.
            </p>
          </section>

          {/* Challenge Preview */}
          <section className="mb-16">
            <h2 className="text-4xl font-black uppercase mb-8 text-center">
              How It Works
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="p-6 bg-white border-4 border-black shadow-brutal-md">
                <div className="text-5xl mb-4">1️⃣</div>
                <h3 className="text-xl font-black uppercase mb-3">Watch Media</h3>
                <p className="font-semibold text-brutal-gray-700">
                  View a video, image, or audio clip carefully
                </p>
              </div>
              <div className="p-6 bg-white border-4 border-black shadow-brutal-md">
                <div className="text-5xl mb-4">2️⃣</div>
                <h3 className="text-xl font-black uppercase mb-3">Analyze</h3>
                <p className="font-semibold text-brutal-gray-700">
                  Look for signs of manipulation and inconsistencies
                </p>
              </div>
              <div className="p-6 bg-white border-4 border-black shadow-brutal-md">
                <div className="text-5xl mb-4">3️⃣</div>
                <h3 className="text-xl font-black uppercase mb-3">Decide</h3>
                <p className="font-semibold text-brutal-gray-700">
                  Make your call: Authentic or Deepfake?
                </p>
              </div>
            </div>
          </section>

          {/* Tips Section */}
          <section className="p-8 bg-brutal-yellow border-4 border-black">
            <h2 className="text-3xl font-black uppercase mb-6">💡 Detection Tips</h2>
            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <span className="text-2xl">👁️</span>
                <span className="font-bold">Watch for unnatural eye movements or blinking patterns</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-2xl">💡</span>
                <span className="font-bold">Check for inconsistent lighting and shadows</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-2xl">🎨</span>
                <span className="font-bold">Look for blurred edges around faces or objects</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-2xl">🔊</span>
                <span className="font-bold">Listen for audio-visual sync issues</span>
              </li>
            </ul>
          </section>
        </div>
      </BrutalPageLayout>
    </>
  );
}
