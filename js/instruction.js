// Instruction page logic
import { getExperimentCondition } from './modules/state.js';

const tutorialBtn = document.getElementById("tutorial-btn");
const contentLines = document.querySelectorAll('.content-line');
const spacebarHint = document.querySelector('.spacebar-hint');
let currentLineIndex = 0;

// Get experiment condition
const condition = getExperimentCondition();
console.log('Instruction page - Condition:', condition);

// Dynamically set content based on condition
function setDynamicContent() {
    const activityOrderContainer = document.getElementById('activity-order-container');
    const submitInstruction = document.getElementById('submit-instruction');
    
    if (condition === 'freeplayFirst') {
        // Free play first: tutorial → free play → puzzles
        if (activityOrderContainer) {
            activityOrderContainer.innerHTML = `
                <p>After getting familiarized with the interface, you will:</p>
                <ol style="margin-left: 1.5rem; margin-top: 0.5rem;">
                    <li style="margin-bottom: 0.5rem;">
                        <strong>Free Play Mode (10 minutes):</strong> Create patterns however you like—no targets, just experiment freely with shapes and operations. Save your creations to a personal gallery. <em style="color: #f59e0b;">You will have 10 minutes to explore and create.</em>
                    </li>
                    <li style="margin-bottom: 0.5rem;">
                        <strong>Pattern Matching (no time limit):</strong> Recreate target patterns as closely as you can using the tools and techniques you've learned. <em style="color: #10b981;">Work at your own pace.</em>
                    </li>
                </ol>
            `;
        }
        if (submitInstruction) {
            submitInstruction.innerHTML = '<strong>For pattern matching:</strong> Submit when you\'ve matched the target exactly, or as closely as you can. <strong>For free play:</strong> Submit when you are happy with your creation.';
        }
    } else {
        // Puzzle first: tutorial → puzzles → free play
        if (activityOrderContainer) {
            activityOrderContainer.innerHTML = `
                <p>After getting familiarized with the interface, you will:</p>
                <ol style="margin-left: 1.5rem; margin-top: 0.5rem;">
                    <li style="margin-bottom: 0.5rem;">
                        <strong>Pattern Matching (no time limit):</strong> Recreate target patterns as closely as you can using primitive shapes and operations. <em style="color: #10b981;">Work at your own pace.</em>
                    </li>
                    <li style="margin-bottom: 0.5rem;">
                        <strong>Free Play Mode (10 minutes):</strong> Create patterns however you like—no targets, just experiment freely with shapes and operations. Save your creations to a personal gallery. <em style="color: #f59e0b;">You will have 10 minutes to explore and create.</em>
                    </li>
                </ol>
            `;
        }
        if (submitInstruction) {
            submitInstruction.innerHTML = '<strong>For pattern matching:</strong> Submit when you\'ve matched the target exactly, or as closely as you can. <strong>For free play:</strong> Submit when you are happy with your creation.';
        }
    }
}

// Tutorial button -> tutorial page
tutorialBtn.onclick = () => location.href = "tutorial.html";

// Show next line when space bar is pressed
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && currentLineIndex < contentLines.length) {
        e.preventDefault(); // Prevent page scroll
        showNextLine();
    }
});

function showNextLine() {
    if (currentLineIndex < contentLines.length) {
        const currentLine = contentLines[currentLineIndex];
        currentLine.classList.remove('hidden');
        currentLine.classList.add('fade-in');
        currentLineIndex++;
        
        // Scroll to the newly revealed line
        setTimeout(() => {
            currentLine.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center'
            });
        }, 100);
        
        // Fade hint after first press
        if (currentLineIndex === 1 && spacebarHint) {
            spacebarHint.style.opacity = '0.5';
        }
        
        // Remove hint and show button when all lines are shown
        if (currentLineIndex === contentLines.length) {
            if (spacebarHint) {
                spacebarHint.style.display = 'none';
            }
            // Show tutorial button
            if (tutorialBtn) {
                tutorialBtn.style.display = 'inline-block';
                tutorialBtn.classList.add('pulse-animation');
            }
        }
    }
}

// Set dynamic content on load
document.addEventListener('DOMContentLoaded', setDynamicContent);
