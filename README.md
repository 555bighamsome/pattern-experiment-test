# Pattern DSL Experiment - Test Version

🧪 This is a **test version** of the Pattern DSL Experiment with counterbalanced design.

## 🚀 Quick Start

### Online Demo (GitHub Pages)
If GitHub Pages is enabled, access the experiment at:
```
https://YOUR_USERNAME.github.io/REPO_NAME/
```

### Local Testing
1. Clone this repository
2. Open `demo_guide.html` in your browser to see the experiment flow
3. Or open `index.html` to start the experiment

## 📋 Experiment Design

This experiment uses a **counterbalanced design** with two conditions:

### Condition 1: Puzzle First
1. Tutorial & Comprehension Check
2. **Puzzle Task** (20 trials) - Pattern matching
3. **Free Play Mode** - Creative pattern design
4. Download combined data

### Condition 2: Free Play First
1. Tutorial & Comprehension Check
2. **Free Play Mode** - Creative pattern design
3. **Puzzle Task** (20 trials) - Pattern matching
4. Download combined data

Participants are **randomly assigned** to one of the two conditions (50/50 split).

## 🎯 Key Features

- ✅ Random condition assignment (persistent across sessions)
- ✅ Dynamic UI based on condition
- ✅ Complete data collection for both phases
- ✅ Simplified tutorial (12 steps + 5 practice exercises)
- ✅ Helper/favorite system with proper isolation between phases
- ✅ Comprehensive data export (JSON format)

## 📂 Project Structure

```
├── index.html                 # Entry point (redirects to consent)
├── demo_guide.html           # Visual guide showing both conditions
├── test_conditions.html      # Testing panel for developers
├── css/
│   └── styles.css           # Main stylesheet
├── js/
│   ├── consent.js
│   ├── instruction.js
│   ├── tutorial.js          # Interactive tutorial (12 steps + 5 practice)
│   ├── comprehension.js     # Comprehension check
│   ├── task.js              # Puzzle task (20 trials)
│   ├── freeplay.js          # Free play mode
│   ├── gallery.js
│   └── modules/
│       ├── state.js         # State management & condition assignment
│       ├── patterns.js      # DSL operations
│       ├── testData.js      # Puzzle patterns
│       └── toast.js         # UI notifications
└── routes/
    ├── consent.html
    ├── instruction.html
    ├── tutorial.html
    ├── comprehension.html
    ├── task.html
    ├── freeplay.html
    ├── gallery.html
    └── reminder.html
```

## 🧪 Testing

### Method 1: Use Demo Guide
Open `demo_guide.html` to see:
- Side-by-side comparison of both conditions
- Quick launch buttons for each condition
- Key design features

### Method 2: Use Test Panel
Open `test_conditions.html` to:
- Manually set conditions
- View current state
- Clear data and reset

### Method 3: Use URL Parameters
- Puzzle First: `index.html?condition=puzzleFirst`
- Free Play First: `index.html?condition=freeplayFirst`
- Random: `index.html`

### Method 4: Use Console Commands
```javascript
// Set condition
localStorage.setItem('experimentCondition', 'puzzleFirst');

// Check condition
console.log(localStorage.getItem('experimentCondition'));

// Clear all data
localStorage.clear();

// Navigate to specific page
location.href = 'routes/task.html';
```

## 📊 Data Collection

The experiment collects comprehensive data including:

### Task Phase Data
- Trial-by-trial performance
- Operation sequences
- Button click actions
- Helper usage
- Timestamps and intervals
- Success/failure rates

### Free Play Phase Data
- Created patterns
- Operation history
- Helper creation and usage
- Session duration
- Gallery of saved patterns

### Final Export
All data is combined into a single JSON file containing both phases, regardless of the order.

## 🔧 Configuration

Key settings in `js/modules/state.js`:
- `SIZE = 10` - Grid size (10×10)
- `POINTS_MAX = 26` - Maximum points (26 trials × 1 point)
- Random condition assignment logic

## 📝 Tutorial Structure

### Interactive Tutorial (Steps 1-12)
1. Blank canvas introduction
2. Add primitive (square)
3. Add primitive (cross)
4. Union operation (combine shapes)
5. Subtract operation
6. Add to helpers
7. Use helper
8. Horizontal flip
9. Vertical flip
10. Rotate operation
11. Binary operation with helper
12. Undo operation

### Practice Exercises (5 puzzles)
1. Perpendicular Cross
2. Union Pattern
3. Diagonal Cross
4. Frame Pattern (flip triangle)
5. Cross Minus Square

## 🎨 Features

- **Pattern DSL**: Visual programming with geometric operations
- **Helpers/Favorites**: Save and reuse pattern components
- **Real-time Preview**: See operation results before applying
- **Undo/Redo**: Full operation history management
- **Gallery**: Save and review created patterns
- **Responsive UI**: Works on different screen sizes

## 📧 Contact

For questions or issues, contact: **s2471381@ed.ac.uk** (Zach)

## 📜 License

This is a research project. All data collected will be used for academic purposes only.

---

**Note**: This is a test version. Always refer to the official repository for the production version.
