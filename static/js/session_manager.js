// frontend/session/session_manager.js

const SESSION_STORAGE_KEY = 'chatbot_session';
const SESSION_MAX_AGE_MS = 30 * 60 * 1000; // 30 minutes

const sessionManager = {
  sessionData: {
    feature: null,
    step: null,
    answers: {},
    timestamp: null
  },

  initializeSession(feature) {
    if (feature !== "quotation") {
      // Only manage sessions for "quotation" feature
      this.clearSession();
      return;
    }
    this.sessionData.feature = feature;
    this.sessionData.step = null;
    this.sessionData.answers = {};
    this.sessionData.timestamp = Date.now();
    this.saveSession();
  },

  saveSession() {
    // Only save session if feature is "quotation"
    if (this.sessionData.feature !== "quotation") {
      this.clearSession();
      return;
    }
    try {
      this.sessionData.timestamp = Date.now();
      const dataString = JSON.stringify(this.sessionData);
      sessionStorage.setItem(SESSION_STORAGE_KEY, dataString);
    } catch (error) {
      console.error('Failed to save session data:', error);
    }
  },

  isExpired(maxAgeMs = SESSION_MAX_AGE_MS) {
    if (!this.sessionData.timestamp) return true;
    return (Date.now() - this.sessionData.timestamp) > maxAgeMs;
  },

  loadSession() {
    try {
      const dataString = sessionStorage.getItem(SESSION_STORAGE_KEY);
      if (dataString) {
        this.sessionData = JSON.parse(dataString);
        // Only keep session if feature is "quotation"
        if (this.sessionData.feature !== "quotation" || this.isExpired()) {
          this.clearSession();
        }
      } else {
        this.sessionData = {
          feature: null,
          step: null,
          answers: {},
          timestamp: null
        };
      }
    } catch (error) {
      console.error('Failed to load session data:', error);
      this.sessionData = {
        feature: null,
        step: null,
        answers: {},
        timestamp: null
      };
    }
    return this.sessionData;
  },

  clearSession() {
    this.sessionData = {
      feature: null,
      step: null,
      answers: {},
      timestamp: null
    };
    sessionStorage.removeItem(SESSION_STORAGE_KEY);
  },

  hasSession() {
    return sessionStorage.getItem(SESSION_STORAGE_KEY) !== null;
  },

  isFeatureActive(feature) {
    return this.sessionData.feature === feature;
  },

  // Additional helper functions for managing steps and answers can be added here
  setStep(step) {
    if (this.sessionData.feature !== "quotation") {
      // Ignore for non-quotation features
      return;
    }
    this.sessionData.step = step;
    this.saveSession();
  },

  setAnswer(questionKey, answer) {
    if (this.sessionData.feature !== "quotation") {
      // Ignore for non-quotation features
      return;
    }
    this.sessionData.answers[questionKey] = answer;
    this.saveSession();
  },

  getAnswer(questionKey) {
    return this.sessionData.answers[questionKey];
  }
};

export default sessionManager;
