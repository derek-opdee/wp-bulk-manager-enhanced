#!/usr/bin/env python3
"""Add opdee.com site directly"""
from wpbm_manager import WPBulkManager

manager = WPBulkManager()
success = manager.add_site("Opdee", "https://opdee.com", "8u5foF2Sbegg5nBRt0IVtL6MhsGufq6U")

if success:
    print("✅ Successfully added opdee.com!")
    print("\nYou can now run: ./run_gui.sh")
else:
    print("❌ Failed to add site")