#!/usr/bin/env python3
"""
Quick viewer for all generated Chapters 1-3 figures
Opens all figures in a systematic way for review
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Configuration
figures_dir = Path('reports/chapters1-3')

# Define all figures
figures = [
    {
        'chapter': 'Chapter 1: Introduction',
        'files': [
            ('Figure 1.1: Framework Architecture', 
             'chapter1/fig1_1_framework_architecture.png')
        ]
    },
    {
        'chapter': 'Chapter 2: Literature Review',
        'files': [
            ('Figure 2.1: ML Approaches Overview', 
             'chapter2/fig2_1_ml_approaches_overview.png')
        ]
    },
    {
        'chapter': 'Chapter 3: Methodology',
        'files': [
            ('Figure 3.1: Complete Five Layer Architecture', 
             'chapter3/fig3_1_complete_five_layer_architecture.png'),
            ('Figure 3.2: Data Flow Diagram', 
             'chapter3/fig3_2_data_flow_diagram.png'),
            ('Figure 3.3: Feature Extraction Pipeline', 
             'chapter3/fig3_3_feature_extraction_pipeline.png'),
            ('Figure 3.4: URL Feature Extraction', 
             'chapter3/fig3_4_url_feature_extraction.png'),
            ('Figure 3.5: Graph-Based Feature Analysis', 
             'chapter3/fig3_5_graph_feature_analysis.png'),
            ('Figure 3.6: VirusTotal Integration', 
             'chapter3/fig3_6_virustotal_integration.png'),
            ('Figure 3.7: Random Forest Architecture', 
             'chapter3/fig3_7_random_forest_architecture.png'),
            ('Figure 3.8: Authentication Risk Model', 
             'chapter3/fig3_8_auth_risk_model.png'),
        ]
    }
]

print("=" * 80)
print("CHAPTERS 1-3 FIGURES VIEWER")
print("=" * 80)
print("\nAvailable viewing options:")
print("  1. View all figures (one by one)")
print("  2. View by chapter")
print("  3. List all figures")
print("  4. Exit")

choice = input("\nEnter your choice (1-4): ").strip()

if choice == '1':
    # View all figures one by one
    print("\n📊 Displaying all figures...")
    print("Close each figure window to see the next one.\n")
    
    for chapter_data in figures:
        print(f"\n{chapter_data['chapter']}")
        print("-" * 60)
        for title, filepath in chapter_data['files']:
            full_path = figures_dir / filepath
            if full_path.exists():
                print(f"  ✓ {title}")
                img = mpimg.imread(full_path)
                plt.figure(figsize=(12, 9))
                plt.imshow(img)
                plt.axis('off')
                plt.title(title, fontsize=14, fontweight='bold', pad=20)
                plt.tight_layout()
                plt.show()
            else:
                print(f"  ✗ {title} - File not found: {filepath}")

elif choice == '2':
    # View by chapter
    print("\nSelect chapter:")
    for i, chapter_data in enumerate(figures, 1):
        print(f"  {i}. {chapter_data['chapter']} ({len(chapter_data['files'])} figures)")
    
    ch = input("\nEnter chapter number: ").strip()
    try:
        ch_idx = int(ch) - 1
        if 0 <= ch_idx < len(figures):
            chapter_data = figures[ch_idx]
            print(f"\n📊 Displaying {chapter_data['chapter']} figures...")
            print("Close each figure window to see the next one.\n")
            
            for title, filepath in chapter_data['files']:
                full_path = figures_dir / filepath
                if full_path.exists():
                    print(f"  ✓ {title}")
                    img = mpimg.imread(full_path)
                    plt.figure(figsize=(12, 9))
                    plt.imshow(img)
                    plt.axis('off')
                    plt.title(title, fontsize=14, fontweight='bold', pad=20)
                    plt.tight_layout()
                    plt.show()
                else:
                    print(f"  ✗ {title} - File not found")
        else:
            print("Invalid chapter number")
    except ValueError:
        print("Invalid input")

elif choice == '3':
    # List all figures
    print("\n" + "=" * 80)
    print("ALL GENERATED FIGURES")
    print("=" * 80)
    
    total = 0
    for chapter_data in figures:
        print(f"\n{chapter_data['chapter']}")
        print("-" * 60)
        for title, filepath in chapter_data['files']:
            full_path = figures_dir / filepath
            status = "✓" if full_path.exists() else "✗"
            print(f"  {status} {title}")
            print(f"      Location: {filepath}")
            if full_path.exists():
                size = full_path.stat().st_size / 1024  # KB
                print(f"      Size: {size:.1f} KB")
                total += 1
    
    print("\n" + "=" * 80)
    print(f"Total figures found: {total}")
    print(f"Output directory: {figures_dir}")
    print("=" * 80)

elif choice == '4':
    print("\n👋 Exiting viewer.")

else:
    print("\n❌ Invalid choice. Please run the script again.")

print("\n💡 Tip: All figures are saved in 'reports/chapters1-3/' directory")
print("   You can also open them directly with any image viewer.\n")
