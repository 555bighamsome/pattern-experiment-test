#!/bin/bash
# Quick setup script for analysis environment

echo "🚀 Setting up analysis environment..."

# Check Python version
python3 --version

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy database config template
if [ ! -f "db_config.py" ]; then
    echo "📝 Creating db_config.py from template..."
    cp db_config.sample.py db_config.py
    echo "⚠️  Please edit db_config.py with your actual database credentials!"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run an analysis:"
echo "  python analyze_experiment_data.py --input ../sample_data.json --plots"
echo ""
