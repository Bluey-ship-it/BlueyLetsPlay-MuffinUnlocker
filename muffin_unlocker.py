#!/usr/bin/env python3
"""
Bluey: Let's Play! - Muffin Unlocker
Unlocks the Muffin character without paying
"""

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Optional


class MuffinUnlocker:
    """Handles unlocking Muffin in Bluey: Let's Play!"""
    
    # Character IDs that need to be unlocked
    MUFFIN_IDS = [
        "muffin",
        "muffin_doll",
        "character_muffin",
    ]
    
    # Save file locations by OS
    SAVE_LOCATIONS = {
        "win32": Path.home() / "AppData" / "Roaming" / "BlueyLetsPlay" / "save.json",
        "darwin": Path.home() / "Library" / "Application Support" / "BlueyLetsPlay" / "save.json",
        "linux": Path.home() / ".config" / "BlueyLetsPlay" / "save.json",
    }
    
    def __init__(self):
        self.save_path: Optional[Path] = None
        self.backup_path: Optional[Path] = None
        
    def find_save_file(self) -> bool:
        """Locate the game's save file"""
        print("🔍 Looking for save file...")
        
        # Try OS-specific location first
        default_save = self.SAVE_LOCATIONS.get(sys.platform)
        if default_save and default_save.exists():
            self.save_path = default_save
            print(f"✓ Found save file at: {self.save_path}")
            return True
        
        # Try alternate locations
        alternate_paths = [
            Path.home() / ".bluey" / "save.json",
            Path.home() / "Documents" / "Bluey" / "save.json",
            Path.home() / "BlueyLetsPlay" / "save.json",
        ]
        
        for path in alternate_paths:
            if path.exists():
                self.save_path = path
                print(f"✓ Found save file at: {self.save_path}")
                return True
        
        print("✗ Could not find save file automatically")
        return False
    
    def prompt_for_save_file(self) -> bool:
        """Prompt user to manually specify save file location"""
        print("\n📂 Please enter the path to your save file:")
        print("   (On Windows: C:\\Users\\YourName\\AppData\\Roaming\\BlueyLetsPlay\\save.json)")
        
        user_path = input("Save file path: ").strip().strip('"\'')
        
        if not user_path:
            return False
        
        path = Path(user_path).expanduser()
        
        if not path.exists():
            print(f"✗ File not found: {path}")
            return False
        
        if not path.suffix.lower() == ".json":
            print("✗ File must be a JSON file")
            return False
        
        self.save_path = path
        print(f"✓ Using save file: {self.save_path}")
        return True
    
    def backup_save_file(self) -> bool:
        """Create a backup of the save file"""
        print("\n💾 Creating backup...")
        
        try:
            backup_dir = self.save_path.parent / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.backup_path = backup_dir / f"save_backup_{timestamp}.json"
            
            shutil.copy2(self.save_path, self.backup_path)
            print(f"✓ Backup created at: {self.backup_path}")
            return True
        except Exception as e:
            print(f"✗ Failed to create backup: {e}")
            return False
    
    def load_save_data(self) -> Optional[dict]:
        """Load the save file JSON"""
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"✗ Save file is corrupted: {e}")
            return None
        except Exception as e:
            print(f"✗ Failed to read save file: {e}")
            return None
    
    def unlock_muffin(self, save_data: dict) -> bool:
        """Unlock Muffin in the save data"""
        print("\n🔓 Unlocking Muffin...")
        
        if "unlocked_characters" not in save_data:
            save_data["unlocked_characters"] = []
        
        unlocked = save_data["unlocked_characters"]
        
        # Add Muffin IDs if not already present
        muffin_unlocked = False
        for muffin_id in self.MUFFIN_IDS:
            if muffin_id not in unlocked:
                unlocked.append(muffin_id)
                muffin_unlocked = True
        
        # Also check for common variations
        if "Muffin" not in unlocked:
            unlocked.append("Muffin")
            muffin_unlocked = True
        
        if not muffin_unlocked:
            print("ℹ️  Muffin is already unlocked!")
            return True
        
        print(f"✓ Muffin unlocked! (Added {len(self.MUFFIN_IDS)} character variants)")
        return True
    
    def save_modified_data(self, save_data: dict) -> bool:
        """Save the modified save file"""
        print("💾 Saving changes...")
        
        try:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            print(f"✓ Save file updated!")
            return True
        except Exception as e:
            print(f"✗ Failed to save changes: {e}")
            if self.backup_path:
                print(f"   Restoring from backup: {self.backup_path}")
                shutil.copy2(self.backup_path, self.save_path)
            return False
    
    def run(self) -> bool:
        """Run the complete unlock process"""
        print("=" * 50)
        print("🎮 Bluey: Let's Play! - Muffin Unlocker")
        print("=" * 50)
        
        # Find save file
        if not self.find_save_file():
            print("\n⚠️  Could not find save file automatically.")
            if not self.prompt_for_save_file():
                print("✗ Aborted: No save file specified")
                return False
        
        # Create backup
        if not self.backup_save_file():
            if input("⚠️  Backup failed. Continue anyway? (y/n): ").lower() != 'y':
                print("✗ Aborted")
                return False
        
        # Load save data
        save_data = self.load_save_data()
        if save_data is None:
            print("✗ Failed to load save file")
            return False
        
        # Unlock Muffin
        if not self.unlock_muffin(save_data):
            print("✗ Failed to unlock Muffin")
            return False
        
        # Save modified data
        if not self.save_modified_data(save_data):
            print("✗ Failed to save changes")
            return False
        
        # Success!
        print("\n" + "=" * 50)
        print("✅ SUCCESS! Muffin has been unlocked!")
        print("=" * 50)
        print("\n📝 Next steps:")
        print("   1. Close the game completely (if it's running)")
        print("   2. Launch Bluey: Let's Play!")
        print("   3. Muffin should now be available as a playable character")
        print("\n💡 If it doesn't work:")
        print(f"   - Restore from backup: {self.backup_path}")
        print("   - Make sure the game was completely closed before unlocking")
        
        return True


def main():
    """Main entry point"""
    unlocker = MuffinUnlocker()
    success = unlocker.run()
    
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
