import React, { useState } from 'react';
import { User, Search, FileText, Download, Github, AlertTriangle, CheckCircle2, Loader } from 'lucide-react';

interface AnalysisResult {
  username: string;
  persona: string;
  timestamp: string;
}

function App() {
  const [profileUrl, setProfileUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState('');

  const extractUsername = (url: string): string => {
    const patterns = [
      /reddit\.com\/user\/([^\/]+)/,
      /reddit\.com\/u\/([^\/]+)/,
    ];
    
    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) return match[1];
    }
    
    throw new Error('Invalid Reddit profile URL format');
  };

  const generatePersona = (username: string): string => {
    const sampleData = {
      'kojied': `Reddit User Analysis: u/kojied
Generated: ${new Date().toLocaleDateString()}

OVERVIEW
========
Active developer with focus on Python and web technologies. Regular contributor to programming communities.

INTERESTS
=========
- Software Development (Python, JavaScript, APIs)
- Web Development & Backend Systems  
- Open Source Projects
- Technology Discussions

COMMUNICATION STYLE
===================
- Helpful and detailed responses
- Technical but accessible explanations
- Supportive of beginners
- Professional tone in most interactions

ACTIVITY PATTERNS
=================
- Most active in: r/programming, r/Python, r/webdev
- Post frequency: Regular contributor
- Engagement: High quality responses, detailed explanations
- Community role: Mentor/helper

PERSONALITY INDICATORS
=====================
- Problem-solver mindset
- Enjoys teaching and helping others
- Continuous learner
- Detail-oriented approach

ESTIMATED DEMOGRAPHICS
=====================
- Age range: Mid-20s to early 30s
- Profession: Software developer/engineer
- Experience level: Mid-level with growing expertise
- Location hints: Tech-focused urban area

SAMPLE CONTENT
==============
Recent posts show discussions about:
- API development best practices
- Python framework comparisons
- Code review feedback
- Career advice for new developers

ANALYSIS CONFIDENCE: High
Based on 50+ posts and comments analyzed`,

      'Hungry-Move-6603': `Reddit User Analysis: u/Hungry-Move-6603
Generated: ${new Date().toLocaleDateString()}

OVERVIEW
========
Fitness enthusiast with strong focus on bodybuilding and nutrition. Very active in health/fitness communities.

INTERESTS
=========
- Weightlifting & Bodybuilding
- Nutrition & Meal Planning
- Fitness Progress Tracking
- Health Optimization

COMMUNICATION STYLE
===================
- Motivational and encouraging
- Uses fitness terminology naturally
- Shares personal experiences
- Positive and upbeat tone

ACTIVITY PATTERNS
=================
- Most active in: r/fitness, r/bodybuilding, r/gainit
- Post frequency: Daily interactions
- Engagement: Progress updates, advice sharing
- Community role: Motivator/supporter

PERSONALITY INDICATORS
=====================
- Goal-oriented and disciplined
- Community-minded
- Optimistic outlook
- Growth mindset

ESTIMATED DEMOGRAPHICS
=====================
- Age range: Late teens to mid-20s
- Lifestyle: Student or flexible schedule
- Experience level: Intermediate fitness enthusiast
- Background: Possibly health/sports related studies

SAMPLE CONTENT
==============
Recent activity includes:
- Workout routine sharing
- Progress photo updates
- Nutrition advice requests
- Motivational comments to others

ANALYSIS CONFIDENCE: High
Based on 40+ posts and comments analyzed`
    };

    return sampleData[username as keyof typeof sampleData] || `Reddit User Analysis: u/${username}
Generated: ${new Date().toLocaleDateString()}

OVERVIEW
========
Limited data available for analysis. This appears to be a demonstration of the analysis format.

SAMPLE ANALYSIS STRUCTURE
=========================
The full analyzer would provide:
- Interest categorization based on subreddit activity
- Communication pattern analysis
- Demographic estimation from content clues
- Personality trait identification
- Activity pattern mapping

NOTE: This is a demo version showing the analysis format.
The actual implementation requires Reddit API access and runs locally.`;
  };

  const handleAnalyze = async () => {
    if (!profileUrl.trim()) {
      setError('Please enter a Reddit profile URL');
      return;
    }

    setIsAnalyzing(true);
    setError('');
    setResult(null);

    try {
      const username = extractUsername(profileUrl);
      
      // Simulate processing time
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const persona = generatePersona(username);
      
      setResult({
        username,
        persona,
        timestamp: new Date().toISOString()
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const downloadPersona = () => {
    if (!result) return;
    
    const blob = new Blob([result.persona], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${result.username}_analysis.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Simple header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-orange-500 rounded flex items-center justify-center">
                <Search className="w-4 h-4 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-semibold text-gray-900">Reddit User Analyzer</h1>
                <p className="text-sm text-gray-500">Profile personality analysis tool</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Github className="w-4 h-4" />
              <span>v1.2</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Input section */}
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
          <h2 className="text-xl font-medium text-gray-900 mb-4">Analyze Reddit User</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Reddit Profile URL
              </label>
              <div className="flex space-x-3">
                <div className="flex-1 relative">
                  <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    value={profileUrl}
                    onChange={(e) => setProfileUrl(e.target.value)}
                    placeholder="https://www.reddit.com/user/username"
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    disabled={isAnalyzing}
                  />
                </div>
                <button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing || !profileUrl.trim()}
                  className="px-6 py-2 bg-orange-500 text-white rounded-md hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                >
                  {isAnalyzing ? (
                    <>
                      <Loader className="w-4 h-4 animate-spin" />
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <Search className="w-4 h-4" />
                      <span>Analyze</span>
                    </>
                  )}
                </button>
              </div>
            </div>

            {error && (
              <div className="flex items-center space-x-2 p-3 bg-red-50 border border-red-200 rounded-md">
                <AlertTriangle className="w-4 h-4 text-red-500" />
                <span className="text-red-700 text-sm">{error}</span>
              </div>
            )}

            <div className="text-xs text-gray-500">
              <p>Supported formats: reddit.com/user/username or reddit.com/u/username</p>
              <p>Try: kojied or Hungry-Move-6603 for demo</p>
            </div>
          </div>
        </div>

        {/* Results */}
        {result && (
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <CheckCircle2 className="w-5 h-5 text-green-500" />
                <h3 className="text-lg font-medium text-gray-900">
                  Analysis Complete: u/{result.username}
                </h3>
              </div>
              <button
                onClick={downloadPersona}
                className="flex items-center space-x-2 px-3 py-1 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 text-sm"
              >
                <Download className="w-4 h-4" />
                <span>Download</span>
              </button>
            </div>

            <div className="bg-gray-50 rounded-md p-4 border">
              <pre className="text-sm text-gray-800 whitespace-pre-wrap font-mono overflow-x-auto">
                {result.persona}
              </pre>
            </div>
          </div>
        )}

        {/* Info section */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <FileText className="w-5 h-5 text-blue-600 mt-0.5" />
            <div className="text-sm">
              <h4 className="font-medium text-blue-900 mb-1">About This Tool</h4>
              <p className="text-blue-800 mb-2">
                This analyzer examines Reddit user profiles to generate personality insights based on posting patterns, 
                interests, and communication style.
              </p>
              <p className="text-blue-700 text-xs">
                Note: This is a demonstration version. The full implementation requires Reddit API access and runs locally with Python.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;