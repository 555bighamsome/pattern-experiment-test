// dataSubmission.js - Handle automatic data submission to server

// PHP endpoint (server-side)
const API_ENDPOINT = 'https://bococo-81.inf.ed.ac.uk/api/save_data.php';

/**
 * Submit experiment data to server
 * @param {Object} data - The experiment data to submit
 * @returns {Promise<Object>} - Server response
 */
async function submitDataToServer(data) {
    try {
        console.log('Submitting data to server...');
        
        // Add metadata
        const payload = {
            participantId: data.participantId || generateParticipantId(),
            condition: data.condition,
            taskData: data.taskData || null,
            freeplayData: data.freeplayData || null,
            userAgent: navigator.userAgent,
            screenResolution: `${window.screen.width}x${window.screen.height}`,
            submissionTime: new Date().toISOString()
        };

        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Data submitted successfully:', result);
        return result;

    } catch (error) {
        console.error('Failed to submit data to server:', error);
        // Return error but don't stop the experiment
        return {
            success: false,
            error: error.message,
            fallbackToDownload: true
        };
    }
}

/**
 * Generate a unique participant ID if not exists
 */
function generateParticipantId() {
    let participantId = localStorage.getItem('participantId');
    if (!participantId) {
        participantId = 'P_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('participantId', participantId);
    }
    return participantId;
}

/**
 * Submit task data when task phase completes
 */
async function submitTaskData() {
    const taskData = localStorage.getItem('taskExperimentData');
    const condition = localStorage.getItem('experimentCondition') || 'puzzleFirst';
    
    if (!taskData) {
        console.warn('No task data to submit');
        return null;
    }

    return await submitDataToServer({
        participantId: generateParticipantId(),
        condition: condition,
        taskData: JSON.parse(taskData),
        freeplayData: null
    });
}

/**
 * Submit freeplay data when freeplay phase completes
 */
async function submitFreeplayData() {
    const freeplayData = localStorage.getItem('freeplayExperimentData');
    const condition = localStorage.getItem('experimentCondition') || 'puzzleFirst';
    
    if (!freeplayData) {
        console.warn('No freeplay data to submit');
        return null;
    }

    return await submitDataToServer({
        participantId: generateParticipantId(),
        condition: condition,
        taskData: null,
        freeplayData: JSON.parse(freeplayData)
    });
}

/**
 * Submit combined data (both task and freeplay)
 */
async function submitCombinedData() {
    const taskData = localStorage.getItem('taskExperimentData');
    const freeplayData = localStorage.getItem('freeplayExperimentData');
    const condition = localStorage.getItem('experimentCondition') || 'puzzleFirst';
    
    const payload = {
        participantId: generateParticipantId(),
        condition: condition,
        taskData: taskData ? JSON.parse(taskData) : null,
        freeplayData: freeplayData ? JSON.parse(freeplayData) : null
    };

    const result = await submitDataToServer(payload);
    
    // If submission failed, offer download as fallback
    if (result.fallbackToDownload) {
        console.log('Server submission failed, offering download as backup...');
        return {
            success: false,
            shouldDownload: true
        };
    }
    
    return result;
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        submitDataToServer,
        submitTaskData,
        submitFreeplayData,
        submitCombinedData,
        generateParticipantId
    };
}
