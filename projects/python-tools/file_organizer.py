#!/usr/bin/env python3
"""
Intelligent File Organizer
A collaborative Python tool for organizing files automatically using AI-powered categorization.
"""

import os
import shutil
import argparse
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import mimetypes

class FileOrganizer:
    """Intelligent file organizer with customizable rules and patterns."""
    
    def __init__(self, config_file: str = "organizer_config.json"):
        self.config_file = config_file
        self.load_config()
        self.stats = {
            "files_processed": 0,
            "files_moved": 0,
            "directories_created": 0,
            "errors": 0
        }
    
    def load_config(self):
        """Load configuration or create default configuration."""
        default_config = {
            "rules": {
                "images": {
                    "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
                    "folder": "Images",
                    "subfolders": {
                        "screenshots": ["screenshot", "screen_shot", "capture"],
                        "photos": ["photo", "img", "picture"],
                        "icons": ["icon", "ico"]
                    }
                },
                "documents": {
                    "extensions": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
                    "folder": "Documents",
                    "subfolders": {
                        "pdfs": [".pdf"],
                        "word_docs": [".doc", ".docx"],
                        "text_files": [".txt", ".rtf"]
                    }
                },
                "videos": {
                    "extensions": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"],
                    "folder": "Videos",
                    "subfolders": {
                        "movies": ["movie", "film"],
                        "tutorials": ["tutorial", "guide", "how_to"]
                    }
                },
                "audio": {
                    "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
                    "folder": "Audio",
                    "subfolders": {
                        "music": ["music", "song"],
                        "podcasts": ["podcast", "episode"],
                        "sounds": ["sound", "sfx", "effect"]
                    }
                },
                "archives": {
                    "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
                    "folder": "Archives"
                },
                "code": {
                    "extensions": [".py", ".js", ".html", ".css", ".cpp", ".java", ".c"],
                    "folder": "Code",
                    "subfolders": {
                        "python": [".py"],
                        "web": [".html", ".css", ".js"],
                        "cpp": [".cpp", ".c", ".h"]
                    }
                }
            },
            "ignore_folders": ["organized", "system", "program files", "windows"],
            "dry_run": False,
            "create_date_folders": True,
            "backup_enabled": True
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                print(f"✅ Loaded configuration from {self.config_file}")
            except json.JSONDecodeError:
                print(f"⚠️  Invalid config file, using defaults")
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
            print(f"📝 Created default configuration at {self.config_file}")
    
    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_file_category(self, file_path: Path) -> Tuple[str, str]:
        """Determine the category and subfolder for a file."""
        file_ext = file_path.suffix.lower()
        file_name = file_path.stem.lower()
        
        for category, rules in self.config["rules"].items():
            if file_ext in rules["extensions"]:
                # Check for subfolder patterns
                if "subfolders" in rules:
                    for subfolder, patterns in rules["subfolders"].items():
                        for pattern in patterns:
                            if pattern in file_name or pattern == file_ext:
                                return category, subfolder
                
                return category, ""
        
        return "misc", ""
    
    def create_organized_structure(self, base_path: Path) -> Dict[str, Path]:
        """Create the organized folder structure."""
        organized_path = base_path / "organized"
        folder_map = {}
        
        for category, rules in self.config["rules"].items():
            category_path = organized_path / rules["folder"]
            
            if not self.config["dry_run"]:
                category_path.mkdir(parents=True, exist_ok=True)
                self.stats["directories_created"] += 1
            
            folder_map[category] = category_path
            
            # Create subfolders
            if "subfolders" in rules:
                for subfolder in rules["subfolders"].keys():
                    subfolder_path = category_path / subfolder
                    if not self.config["dry_run"]:
                        subfolder_path.mkdir(exist_ok=True)
                        self.stats["directories_created"] += 1
                    folder_map[f"{category}_{subfolder}"] = subfolder_path
        
        # Create misc folder
        misc_path = organized_path / "Miscellaneous"
        if not self.config["dry_run"]:
            misc_path.mkdir(parents=True, exist_ok=True)
        folder_map["misc"] = misc_path
        
        return folder_map
    
    def should_ignore_folder(self, folder_name: str) -> bool:
        """Check if folder should be ignored."""
        folder_lower = folder_name.lower()
        return any(ignore in folder_lower for ignore in self.config["ignore_folders"])
    
    def organize_directory(self, source_path: str, recursive: bool = False):
        """Organize files in the specified directory."""
        source = Path(source_path).resolve()
        
        if not source.exists():
            print(f"❌ Source directory '{source}' does not exist!")
            return
        
        print(f"🚀 Starting file organization in: {source}")
        print(f"📊 Mode: {'DRY RUN' if self.config['dry_run'] else 'LIVE'}")
        print("-" * 60)
        
        # Create organized structure
        folder_map = self.create_organized_structure(source)
        
        # Get all files to process
        files_to_process = []
        
        if recursive:
            for root, dirs, files in os.walk(source):
                # Skip ignored folders
                dirs[:] = [d for d in dirs if not self.should_ignore_folder(d)]
                
                for file in files:
                    file_path = Path(root) / file
                    # Skip files already in organized folder
                    if "organized" not in str(file_path):
                        files_to_process.append(file_path)
        else:
            files_to_process = [f for f in source.iterdir() if f.is_file()]
        
        # Process files
        for file_path in files_to_process:
            try:
                self.organize_file(file_path, folder_map)
                self.stats["files_processed"] += 1
            except Exception as e:
                print(f"❌ Error processing {file_path.name}: {e}")
                self.stats["errors"] += 1
        
        self.print_summary()
    
    def organize_file(self, file_path: Path, folder_map: Dict[str, Path]):
        """Organize a single file."""
        category, subfolder = self.get_file_category(file_path)
        
        # Determine destination
        if subfolder:
            dest_folder = folder_map.get(f"{category}_{subfolder}", folder_map[category])
        else:
            dest_folder = folder_map[category]
        
        # Add date folder if enabled
        if self.config["create_date_folders"]:
            file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
            date_folder = dest_folder / file_date.strftime("%Y-%m")
            
            if not self.config["dry_run"]:
                date_folder.mkdir(exist_ok=True)
            
            dest_folder = date_folder
        
        # Handle filename conflicts
        dest_path = dest_folder / file_path.name
        counter = 1
        while dest_path.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            dest_path = dest_folder / f"{stem}_{counter}{suffix}"
            counter += 1
        
        # Move or copy file
        action = "MOVE" if not self.config["backup_enabled"] else "COPY"
        print(f"📁 {action}: {file_path.name} → {dest_path.relative_to(file_path.parent.parent)}")
        
        if not self.config["dry_run"]:
            if self.config["backup_enabled"]:
                shutil.copy2(file_path, dest_path)
            else:
                shutil.move(str(file_path), str(dest_path))
            self.stats["files_moved"] += 1
    
    def print_summary(self):
        """Print organization summary."""
        print("\n" + "=" * 60)
        print("📊 ORGANIZATION SUMMARY")
        print("=" * 60)
        print(f"Files processed: {self.stats['files_processed']}")
        print(f"Files moved/copied: {self.stats['files_moved']}")
        print(f"Directories created: {self.stats['directories_created']}")
        print(f"Errors: {self.stats['errors']}")
        
        if self.config["dry_run"]:
            print("\n⚠️  This was a DRY RUN - no files were actually moved!")
            print("Run with --execute to perform the actual organization.")
    
    def analyze_directory(self, path: str):
        """Analyze directory contents without organizing."""
        source = Path(path)
        analysis = {}
        
        for file_path in source.rglob("*"):
            if file_path.is_file():
                category, subfolder = self.get_file_category(file_path)
                key = f"{category}/{subfolder}" if subfolder else category
                
                if key not in analysis:
                    analysis[key] = {"count": 0, "size": 0, "files": []}
                
                analysis[key]["count"] += 1
                analysis[key]["size"] += file_path.stat().st_size
                analysis[key]["files"].append(file_path.name)
        
        # Print analysis
        print(f"\n📊 DIRECTORY ANALYSIS: {source}")
        print("=" * 60)
        
        for category, data in sorted(analysis.items()):
            size_mb = data["size"] / (1024 * 1024)
            print(f"📁 {category}: {data['count']} files ({size_mb:.1f} MB)")
            
            if len(data["files"]) <= 5:
                for file in data["files"]:
                    print(f"   • {file}")
            else:
                for file in data["files"][:3]:
                    print(f"   • {file}")
                print(f"   ... and {len(data['files']) - 3} more")
            print()

def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="🤖 Intelligent File Organizer - Collaborative AI-Human Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python organizer.py ~/Downloads --execute
  python organizer.py ~/Desktop --dry-run --recursive
  python organizer.py ~/Documents --analyze
  python organizer.py ~/Pictures --config my_rules.json
        """
    )
    
    parser.add_argument("directory", help="Directory to organize")
    parser.add_argument("--execute", action="store_true", help="Execute the organization (default is dry run)")
    parser.add_argument("--recursive", "-r", action="store_true", help="Organize files recursively")
    parser.add_argument("--analyze", "-a", action="store_true", help="Analyze directory without organizing")
    parser.add_argument("--config", "-c", default="organizer_config.json", help="Configuration file")
    parser.add_argument("--backup", action="store_true", help="Copy files instead of moving them")
    parser.add_argument("--no-date-folders", action="store_true", help="Don't create date-based subfolders")
    
    args = parser.parse_args()
    
    # Create organizer instance
    organizer = FileOrganizer(args.config)
    
    # Update config based on arguments
    if not args.execute:
        organizer.config["dry_run"] = True
    
    if args.backup:
        organizer.config["backup_enabled"] = True
    
    if args.no_date_folders:
        organizer.config["create_date_folders"] = False
    
    # Print header
    print("🤖🤝👨‍💻 INTELLIGENT FILE ORGANIZER")
    print("=" * 60)
    print("A collaborative AI-human tool for smart file organization")
    print("=" * 60)
    
    if args.analyze:
        organizer.analyze_directory(args.directory)
    else:
        organizer.organize_directory(args.directory, args.recursive)
    
    print("\n💡 Tip: You can customize organization rules by editing the config file!")
    print(f"📝 Config file: {organizer.config_file}")

if __name__ == "__main__":
    main()