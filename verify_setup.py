#!/usr/bin/env python3
"""
Setup Verification Script for Invoice Payment Manager
Run this to verify your installation is complete and ready to use.
"""

import sys
import os
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_check(condition, success_msg, fail_msg):
    """Print a check result"""
    if condition:
        print(f"✅ {success_msg}")
        return True
    else:
        print(f"❌ {fail_msg}")
        return False

def verify_python_version():
    """Check Python version"""
    version = sys.version_info
    return version.major >= 3 and version.minor >= 8

def verify_files():
    """Check if all required files exist"""
    required_files = [
        'main_simple.py',
        'config.py',
        'data_manager.py',
        'ai_decision_engine.py',
        'email_generator.py',
        'styles.py',
        'requirements.txt',
        'run.sh',
        'README.md'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    return len(missing) == 0, missing

def verify_data_files():
    """Check if data directory and CSV files exist"""
    if not os.path.exists('data'):
        return False, "Data directory not found"
    
    csv_files = ['invoice_requests.csv', 'decisions.csv', 'audit_log.csv']
    missing = []
    for file in csv_files:
        if not os.path.exists(f'data/{file}'):
            missing.append(file)
    
    if missing:
        return False, f"Missing: {', '.join(missing)}"
    return True, "All CSV files present"

def verify_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'streamlit': 'streamlit',
        'pandas': 'pandas',
        'plotly': 'plotly',
        'numpy': 'numpy',
    }
    
    missing = []
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package)
    
    return len(missing) == 0, missing

def verify_csv_data():
    """Verify CSV files have data"""
    try:
        with open('data/invoice_requests.csv', 'r') as f:
            lines = len(f.readlines())
            requests_count = lines - 1  # Minus header
        
        with open('data/decisions.csv', 'r') as f:
            lines = len(f.readlines())
            decisions_count = lines - 1
        
        with open('data/audit_log.csv', 'r') as f:
            lines = len(f.readlines())
            audit_count = lines - 1
        
        return True, (requests_count, decisions_count, audit_count)
    except Exception as e:
        return False, str(e)

def main():
    """Run all verification checks"""
    
    print("\n" + "🔍 INVOICE PAYMENT MANAGER - SETUP VERIFICATION" + "\n")
    print("This script will verify your installation is complete.\n")
    
    all_passed = True
    
    # Check 1: Python Version
    print_header("1. Python Version Check")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if print_check(
        verify_python_version(),
        f"Python {version_str} (meets requirement: 3.8+)",
        f"Python {version_str} is too old (need 3.8+)"
    ):
        pass
    else:
        all_passed = False
        print("   💡 Upgrade Python: https://www.python.org/downloads/")
    
    # Check 2: Core Files
    print_header("2. Core Application Files")
    files_ok, missing = verify_files()
    
    if print_check(
        files_ok,
        "All 9 core files present",
        f"Missing files: {', '.join(missing)}"
    ):
        print("   ✓ main_simple.py")
        print("   ✓ config.py")
        print("   ✓ data_manager.py")
        print("   ✓ ai_decision_engine.py")
        print("   ✓ email_generator.py")
        print("   ✓ styles.py")
        print("   ✓ requirements.txt")
        print("   ✓ run.sh")
        print("   ✓ README.md")
    else:
        all_passed = False
        print("   💡 Re-download missing files from repository")
    
    # Check 3: Data Files
    print_header("3. Data Directory & CSV Files")
    data_ok, message = verify_data_files()
    
    if print_check(
        data_ok,
        "Data directory with 3 CSV files",
        message
    ):
        csv_ok, counts = verify_csv_data()
        if csv_ok:
            requests, decisions, audit = counts
            print(f"   ✓ invoice_requests.csv ({requests} records)")
            print(f"   ✓ decisions.csv ({decisions} records)")
            print(f"   ✓ audit_log.csv ({audit} records)")
        else:
            print(f"   ⚠️  CSV files exist but may be empty or corrupted")
    else:
        all_passed = False
        print("   💡 Run: python3 generate_sample_data.py")
    
    # Check 4: Dependencies
    print_header("4. Python Package Dependencies")
    deps_ok, missing = verify_dependencies()
    
    if print_check(
        deps_ok,
        "All required packages installed",
        f"Missing packages: {', '.join(missing)}"
    ):
        print("   ✓ streamlit")
        print("   ✓ pandas")
        print("   ✓ plotly")
        print("   ✓ numpy")
    else:
        all_passed = False
        print("   💡 Run: pip3 install -r requirements.txt")
    
    # Check 5: File Permissions
    print_header("5. File Permissions")
    run_sh_executable = os.access('run.sh', os.X_OK)
    
    if print_check(
        run_sh_executable,
        "run.sh is executable",
        "run.sh is not executable"
    ):
        pass
    else:
        print("   💡 Run: chmod +x run.sh")
    
    # Check 6: Documentation
    print_header("6. Documentation Files")
    doc_files = ['README.md', 'QUICKSTART.md', 'TESTING_CHECKLIST.md', 'PROJECT_SUMMARY.md']
    doc_exists = [os.path.exists(f) for f in doc_files]
    
    if print_check(
        all(doc_exists),
        "All documentation files present",
        "Some documentation files missing"
    ):
        for i, file in enumerate(doc_files):
            if doc_exists[i]:
                size = os.path.getsize(file) / 1024
                print(f"   ✓ {file} ({size:.1f} KB)")
    
    # Final Summary
    print_header("VERIFICATION SUMMARY")
    
    if all_passed:
        print("\n🎉 SUCCESS! Your installation is complete and ready to use.\n")
        print("Next Steps:")
        print("  1. Launch the application:")
        print("     ./run.sh")
        print("     OR")
        print("     streamlit run main_simple.py")
        print()
        print("  2. Open your browser to:")
        print("     http://localhost:8501")
        print()
        print("  3. Read QUICKSTART.md for a guided tour")
        print()
    else:
        print("\n⚠️  ISSUES FOUND - Please address the items marked with ❌ above.\n")
        print("Common Fixes:")
        print("  • Install dependencies: pip3 install -r requirements.txt")
        print("  • Generate data: python3 generate_sample_data.py")
        print("  • Fix permissions: chmod +x run.sh")
        print()
        print("After fixing, run this script again to verify.\n")
    
    print("="*60)
    print()
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

