#!/usr/bin/env python3
"""
Test imports and module structure for WP Bulk Manager v2
"""
import os
import sys

# Add the wpbm package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing WP Bulk Manager v2 imports...")
print("="*60)

# Test each module
modules_to_test = [
    ("Core Package", "wpbm"),
    ("API Client", "wpbm.api.client"),
    ("API Auth", "wpbm.api.auth"),
    ("Content Operations", "wpbm.operations.content"),
    ("Media Operations", "wpbm.operations.media"),
    ("Logger Utility", "wpbm.utils.logger"),
    ("Cache Manager", "wpbm.utils.cache"),
    ("Main Manager v2", "wpbm_manager_v2")
]

successful_imports = []
failed_imports = []

for name, module_path in modules_to_test:
    try:
        module = __import__(module_path, fromlist=[''])
        successful_imports.append((name, module_path))
        print(f"✅ {name} ({module_path})")
        
        # Check for specific classes/functions
        if module_path == "wpbm.api.client":
            if hasattr(module, 'WPBMClient'):
                print(f"   - Found WPBMClient class")
        elif module_path == "wpbm.api.auth":
            if hasattr(module, 'APIKeyManager'):
                print(f"   - Found APIKeyManager class")
        elif module_path == "wpbm.operations.content":
            if hasattr(module, 'ContentOperations'):
                print(f"   - Found ContentOperations class")
        elif module_path == "wpbm.operations.media":
            if hasattr(module, 'MediaOperations'):
                print(f"   - Found MediaOperations class")
        elif module_path == "wpbm.utils.cache":
            if hasattr(module, 'CacheManager'):
                print(f"   - Found CacheManager class")
                
    except ImportError as e:
        failed_imports.append((name, module_path, str(e)))
        print(f"❌ {name} ({module_path})")
        print(f"   Error: {e}")

print("\n" + "="*60)
print("IMPORT SUMMARY")
print("="*60)
print(f"Successful imports: {len(successful_imports)}")
print(f"Failed imports: {len(failed_imports)}")

if failed_imports:
    print("\n⚠️  Some imports failed. Check the following:")
    for name, module, error in failed_imports:
        print(f"  - {name}: {error}")
else:
    print("\n✅ All imports successful! The package structure is correct.")

# Test instantiation
print("\n" + "="*60)
print("TESTING INSTANTIATION")
print("="*60)

try:
    from wpbm_manager_v2 import WPBulkManagerV2
    manager = WPBulkManagerV2()
    print("✅ WPBulkManagerV2 instantiated successfully")
    
    # Check database
    if os.path.exists(manager.db_path):
        print(f"✅ Database exists at: {manager.db_path}")
    else:
        print(f"⚠️  Database not found at: {manager.db_path}")
        
except Exception as e:
    print(f"❌ Failed to instantiate WPBulkManagerV2: {e}")

print("\n" + "="*60)
print("Test complete!")