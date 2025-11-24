export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  // for LiveKit Cloud Sandbox
  sandboxId?: string;
  agentName?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Teach-the-Tutor',
  pageTitle: 'Active Recall Coach',
  pageDescription: 'Learn, Quiz, and Teach Back with your AI Tutor',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/lk-logo.svg',
  accent: '#6366f1', // Indigo-500
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#818cf8', // Indigo-400
  startButtonText: 'Start Learning Session',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
