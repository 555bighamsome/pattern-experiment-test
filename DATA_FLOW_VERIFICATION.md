# Data Flow Verification Guide

## Overview
This document explains how experiment data is collected, stored, and submitted in both experiment conditions.

## Data Collection Points

### Task Phase (task.js)
**What is collected:**
- `allTrialsData` array containing:
  - `metadata`: Trial order, randomization, points system
  - Per-trial data:
    - `trial`: Trial number
    - `targetPattern`: Target pattern to match
    - `steps[]`: Every operation with timestamp, pattern state, operands
    - `operations[]`: String representation of operations
    - `stepsCount`: Number of operations used
    - `timeSpent`: Time in milliseconds
    - `success`: Whether trial was correct
    - `submitted`: Whether trial was submitted
    - `pointsEarned`: Points earned for this trial
    - `pointsAwarded`: Points awarded in this submission

**When data is saved to localStorage:**
- **puzzleFirst condition**: When user completes all trials and clicks "Submit & Exit", `enterFreePlayMode()` saves to `localStorage.setItem('taskExperimentData', ...)`
- **freeplayFirst condition**: When user completes all trials and clicks "Submit & Exit", `handleTaskCompletion()` saves to `localStorage.setItem('taskExperimentData', ...)`

### Freeplay Phase (freeplay.js)
**What is collected:**
- `freeplaySessions` array (saved to localStorage after each session)
- Per-session data (`sessionRecord`):
  - `sessionId`: Unique session identifier
  - `startTime`, `endTime`, `totalDuration`
  - `buttonClickActions[]`: Every button click with context
  - `operationActions[]`: Every operation with operands and results
  - `patternsCreated[]`: Reference to gallery items created
  - `finalPattern`: Final pattern in workspace
  - `helperUsageCount`: Count of helper pattern usage

**Gallery data:**
- Saved separately to `localStorage` as `patternGallery`
- Each item contains:
  - Pattern JSON
  - Operations history
  - Timestamp
  - User-provided name (optional)
  - Session ID reference

**When data is saved to localStorage:**
- Sessions: Automatically saved to `freeplaySessions` during freeplay
- Combined export: When user clicks completion button, `handleFreeplayCompletion()` creates and saves `freeplayExperimentData` containing:
  - `sessions`: All freeplay sessions
  - `gallery`: All saved patterns
  - `helpers`: All helper patterns
  - `completionTime`: Timestamp

## Data Submission Flow

### Condition 1: puzzleFirst
1. **Start**: User begins with Task phase
2. **Task completion**: 
   - User completes all trials
   - Clicks "Submit & Exit"
   - `handleTaskCompletion()` saves task data to localStorage
   - If in puzzleFirst, redirects to Freeplay via `enterFreePlayMode()`
3. **Freeplay phase**:
   - User creates patterns for 10 minutes
   - Timer expires, `endFreePlayMode()` shows modal
4. **Final submission**:
   - User clicks "✓ Submit Data"
   - `handleFreeplayCompletion()` detects puzzleFirst condition
   - Saves freeplay data to localStorage
   - Calls `submitCombinedData()` which:
     - Reads `taskExperimentData` from localStorage
     - Reads `freeplayExperimentData` from localStorage
     - Sends POST to `https://bococo-81.inf.ed.ac.uk/api/save_data.php`
   - On success: Shows success message
   - On failure: Falls back to download

### Condition 2: freeplayFirst
1. **Start**: User begins with Freeplay phase
2. **Freeplay completion**:
   - User creates patterns for 10 minutes
   - Timer expires, `endFreePlayMode()` shows modal
   - User clicks "→ Continue to Puzzle Phase"
   - `handleFreeplayCompletion()` detects freeplayFirst condition
   - Saves freeplay data to localStorage
   - Redirects to Task phase
3. **Task phase**:
   - User completes all trials
   - Clicks "Submit & Exit"
4. **Final submission**:
   - `handleTaskCompletion()` saves task data to localStorage
   - Calls `submitCombinedData()` which:
     - Reads `taskExperimentData` from localStorage
     - Reads `freeplayExperimentData` from localStorage (saved earlier)
     - Sends POST to server
   - On success: Shows success message
   - On failure: Falls back to download

## Database Schema

### Table: `experiment_data`
```sql
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- participant_id (VARCHAR(100))
- condition (VARCHAR(50))  -- 'puzzleFirst' or 'freeplayFirst'
- submission_time (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- task_data (JSON)         -- allTrialsData from task phase
- freeplay_data (JSON)     -- sessionData from freeplay phase
- user_agent (TEXT)
- screen_resolution (VARCHAR(50))
```

## API Payload Structure

```json
{
  "participantId": "P_1234567890_abc123xyz",
  "condition": "puzzleFirst" | "freeplayFirst",
  "taskData": {
    // allTrialsData array
  },
  "freeplayData": {
    "sessions": [],
    "gallery": [],
    "helpers": [],
    "completionTime": "2025-12-21T10:30:00.000Z"
  },
  "userAgent": "Mozilla/5.0...",
  "screenResolution": "1920x1080",
  "submissionTime": "2025-12-21T10:30:00.000Z"
}
```

## Key Files Modified

1. **routes/task.html**
   - `handleTaskCompletion()`: Saves task data before submission

2. **routes/freeplay.html**
   - `handleFreeplayCompletion()`: 
     - Saves freeplay data
     - Detects condition to either redirect or submit

3. **js/freeplay.js**
   - `endFreePlayMode()`: Updates button text based on condition

4. **js/dataSubmission.js**
   - `submitCombinedData()`: Reads both datasets from localStorage and submits

## Testing Checklist

### puzzleFirst Flow:
- [ ] Complete at least 1 task trial
- [ ] Click "Submit & Exit" in task
- [ ] Verify redirect to freeplay
- [ ] Create at least 1 pattern in freeplay
- [ ] Wait for 10-minute timer or manually end
- [ ] Verify modal shows "✓ Submit Data"
- [ ] Click submit button
- [ ] Check database for new row with both task_data and freeplay_data populated

### freeplayFirst Flow:
- [ ] Create at least 1 pattern in freeplay
- [ ] Wait for 10-minute timer or manually end
- [ ] Verify modal shows "→ Continue to Puzzle Phase"
- [ ] Click continue button
- [ ] Verify redirect to task
- [ ] Complete at least 1 task trial
- [ ] Click "Submit & Exit"
- [ ] Check database for new row with both task_data and freeplay_data populated

## Common Issues & Solutions

### Issue: NULL data in database
**Cause**: Data not saved to localStorage before submission
**Solution**: Ensure `handleTaskCompletion()` and `handleFreeplayCompletion()` save data before calling `submitCombinedData()`

### Issue: Only one dataset (task or freeplay) is populated
**Cause**: Wrong submission timing or condition detection
**Solution**: 
- puzzleFirst: Submit only after freeplay completes
- freeplayFirst: Ensure freeplay data saved before redirect to task

### Issue: 403 CORS error
**Cause**: Origin not whitelisted in save_data.php
**Solution**: Add origin to `$allowed_origins` array in save_data.php

## Verification Commands

Check localStorage in browser console:
```javascript
// Check what's stored
console.log('Task data:', localStorage.getItem('taskExperimentData'));
console.log('Freeplay data:', localStorage.getItem('freeplayExperimentData'));
console.log('Condition:', localStorage.getItem('experimentCondition'));
console.log('Participant ID:', localStorage.getItem('participantId'));

// Check data sizes
console.log('Task data size:', localStorage.getItem('taskExperimentData')?.length);
console.log('Freeplay data size:', localStorage.getItem('freeplayExperimentData')?.length);
```

Check database via phpMyAdmin:
```sql
SELECT 
    id,
    participant_id,
    `condition`,
    submission_time,
    JSON_LENGTH(task_data) as task_items,
    JSON_LENGTH(freeplay_data, '$.sessions') as freeplay_sessions,
    JSON_LENGTH(freeplay_data, '$.gallery') as gallery_items
FROM experiment_data
ORDER BY id DESC
LIMIT 10;
```
