const SIZE = 10;
const CELL_SIZE = 40;
const POINTS_MAX = 25; // 1 point per trial (25 trials total, Pattern-23 removed)

// Normalize condition string to handle case variations and whitespace
function normalizeCondition(condition) {
    if (!condition) return null;
    
    // Trim whitespace and convert to lowercase for comparison
    const normalized = condition.trim().toLowerCase();
    
    // Return standardized format
    if (normalized === 'puzzlefirst') {
        return 'puzzleFirst';
    } else if (normalized === 'freeplayfirst') {
        return 'freeplayFirst';
    }
    
    // Return as-is if already in correct format
    return condition.trim();
}

// Initialize or retrieve experiment condition
function getExperimentCondition() {
    let condition = localStorage.getItem('experimentCondition');
    
    if (!condition) {
        // Random assignment: 50% puzzleFirst, 50% freeplayFirst
        condition = Math.random() < 0.5 ? 'puzzleFirst' : 'freeplayFirst';
        localStorage.setItem('experimentCondition', condition);
        console.log('Assigned new condition:', condition);
    } else {
        // Normalize existing condition to fix any formatting issues
        const normalized = normalizeCondition(condition);
        if (normalized !== condition) {
            console.log('Normalized condition from', condition, 'to', normalized);
            localStorage.setItem('experimentCondition', normalized);
            condition = normalized;
        }
    }
    
    return condition;
}

const appState = {
    currentTestIndex: 0,
    currentPattern: null,
    targetPattern: null,
    operationsHistory: [],
    workflowSelections: [],
    pendingBinaryOp: null,
    pendingUnaryOp: null,
    previewPattern: null,
    previewBackupPattern: null,
    pointsPerCorrect: 0,
    totalPoints: 0,
    favorites: [],
    inlinePreview: null,
    unaryPreviewState: null,
    unaryModeJustEntered: false,
    allTrialsData: [],
    trialStartTime: null,
    testOrder: [],
    shouldRandomize: false,
    currentTrialRecord: null,
    experimentCondition: getExperimentCondition(),
    // Trial history for viewing previous trial
    previousTrialHistory: null,
    currentTrialHistory: null,
    isViewingPreviousTrial: false
};

const globalScope = typeof window !== 'undefined' ? window : globalThis;

const stateBindings = [
    'currentTestIndex',
    'currentPattern',
    'targetPattern',
    'operationsHistory',
    'workflowSelections',
    'pendingBinaryOp',
    'pendingUnaryOp',
    'previewPattern',
    'previewBackupPattern',
    'pointsPerCorrect',
    'totalPoints',
    'favorites',
    'inlinePreview',
    'unaryPreviewState',
    'unaryModeJustEntered',
    'allTrialsData',
    'trialStartTime',
    'testOrder',
    'shouldRandomize',
    'currentTrialRecord',
    'experimentCondition'
];

stateBindings.forEach((key) => {
    Object.defineProperty(globalScope, key, {
        configurable: false,
        enumerable: false,
        get() {
            return appState[key];
        },
        set(value) {
            appState[key] = value;
        }
    });
});

let tutorialMode = false;

export {
    SIZE,
    CELL_SIZE,
    POINTS_MAX,
    appState,
    stateBindings,
    globalScope,
    getExperimentCondition
};

export function isTutorialMode() {
    return tutorialMode;
}

export function setTutorialMode(value) {
    tutorialMode = Boolean(value);
}

export function checkTutorialProgress() {
    // no-op placeholder retained for legacy calls
}
