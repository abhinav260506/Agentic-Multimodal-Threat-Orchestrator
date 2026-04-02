"""
Main Processing Script for Lightweight AgenticCyber Framework
Processes input files from input/ folder and saves results to output/ folder
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import config
from log_agent import LogAgent
from vision_agent import VisionAgent
from network_agent import NetworkAgent
from main_orchestrator import CyberOrchestrator


class InputProcessor:
    """Processes input files and generates output reports"""
    
    def __init__(self):
        self.input_dir = config.INPUT_DIR
        self.output_dir = config.OUTPUT_DIR
        self.orchestrator = CyberOrchestrator()
        self.results = {}
    
    def find_input_files(self) -> Dict[str, List[Path]]:
        """Find all input files in the input directory"""
        files = {
            'logs': list(config.INPUT_LOGS_DIR.glob("*.csv")),
            'videos': list(config.INPUT_VIDEOS_DIR.glob("*.mp4")),
            'network': list(config.INPUT_NETWORK_DIR.glob("*.txt")) if config.INPUT_NETWORK_DIR.exists() else []
        }
        return files
    
    def process_all(self) -> Dict[str, Any]:
        """Process all input files and generate comprehensive report"""
        print("="*60)
        print("PROCESSING INPUT FILES")
        print("="*60)
        
        # Find input files
        input_files = self.find_input_files()
        
        # Check if any files exist
        total_files = sum(len(files) for files in input_files.values())
        if total_files == 0:
            print("\n[WARNING] No input files found!")
            print(f"Please place files in:")
            print(f"  - Logs: {config.INPUT_LOGS_DIR}")
            print(f"  - Videos: {config.INPUT_VIDEOS_DIR}")
            print(f"  - Network: {config.INPUT_NETWORK_DIR}")
            return {}
        
        print(f"\nFound input files:")
        print(f"  - Log files: {len(input_files['logs'])}")
        print(f"  - Video files: {len(input_files['videos'])}")
        print(f"  - Network files: {len(input_files['network'])}")
        
        # Process each type
        results = {
            'timestamp': datetime.now().isoformat(),
            'log_analysis': [],
            'vision_analysis': [],
            'network_analysis': [],
            'final_assessment': None
        }
        
        # Process log files
        if input_files['logs']:
            print(f"\n{'='*60}")
            print("PROCESSING LOG FILES")
            print(f"{'='*60}")
            for log_file in input_files['logs']:
                print(f"\nAnalyzing: {log_file.name}")
                result = self.process_log_file(log_file)
                results['log_analysis'].append({
                    'file': log_file.name,
                    'result': result
                })
        
        # Process video files
        if input_files['videos']:
            print(f"\n{'='*60}")
            print("PROCESSING VIDEO FILES")
            print(f"{'='*60}")
            for video_file in input_files['videos']:
                print(f"\nAnalyzing: {video_file.name}")
                result = self.process_video_file(video_file)
                results['vision_analysis'].append({
                    'file': video_file.name,
                    'result': result
                })
        
        # Process network (if files exist, otherwise use live system)
        print(f"\n{'='*60}")
        print("PROCESSING NETWORK ANALYSIS")
        print(f"{'='*60}")
        if input_files['network']:
            for network_file in input_files['network']:
                print(f"\nAnalyzing: {network_file.name}")
                result = self.process_network_file(network_file)
                results['network_analysis'].append({
                    'file': network_file.name,
                    'result': result
                })
        else:
            print("\nNo network files found. Using live system analysis...")
            result = self.process_network_live()
            results['network_analysis'].append({
                'file': 'live_system',
                'result': result
            })
        
        # Generate final assessment
        print(f"\n{'='*60}")
        print("GENERATING FINAL ASSESSMENT")
        print(f"{'='*60}")
        final_assessment = self.generate_final_assessment(results)
        results['final_assessment'] = final_assessment
        
        # Save results
        self.save_results(results)
        
        # Print summary
        self.print_summary(results)
        
        return results
    
    def process_log_file(self, log_file: Path) -> Dict[str, Any]:
        """Process a single log file"""
        log_agent = LogAgent()
        result = log_agent.analyze(log_file=log_file, sample_size=10000)
        return result
    
    def process_video_file(self, video_file: Path) -> Dict[str, Any]:
        """Process a single video file"""
        vision_agent = VisionAgent()
        result = vision_agent.analyze(video_path=video_file, frame_time_ms=1000)
        return result
    
    def process_network_file(self, network_file: Path) -> Dict[str, Any]:
        """Process a network data file"""
        # For now, use live network agent
        # Can be extended to read from file
        network_agent = NetworkAgent()
        result = network_agent.analyze()
        return result
    
    def process_network_live(self) -> Dict[str, Any]:
        """Process live network data"""
        network_agent = NetworkAgent()
        result = network_agent.analyze()
        return result
    
    def generate_final_assessment(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final unified assessment from all results"""
        # Collect all threat levels
        threat_levels = []
        details_list = []
        
        # From log analysis
        for log_result in results.get('log_analysis', []):
            threat_levels.append(log_result['result'].get('threat_level', 'SECURE'))
            details_list.append(f"Logs ({log_result['file']}): {log_result['result'].get('details', '')}")
        
        # From vision analysis
        for vision_result in results.get('vision_analysis', []):
            threat_levels.append(vision_result['result'].get('threat_level', 'SECURE'))
            details_list.append(f"Video ({vision_result['file']}): {vision_result['result'].get('details', '')}")
        
        # From network analysis
        for network_result in results.get('network_analysis', []):
            threat_levels.append(network_result['result'].get('threat_level', 'SECURE'))
            details_list.append(f"Network ({network_result['file']}): {network_result['result'].get('details', '')}")
        
        # Determine overall threat level
        if 'CRITICAL' in threat_levels:
            overall_threat = 'CRITICAL'
        elif 'WARNING' in threat_levels:
            overall_threat = 'WARNING'
        else:
            overall_threat = 'SECURE'
        
        # Use orchestrator for final fusion if available
        try:
            # Prepare agent results for orchestrator
            self.orchestrator.results = {}
            if results.get('log_analysis'):
                self.orchestrator.results['log'] = results['log_analysis'][0]['result']
            if results.get('vision_analysis'):
                self.orchestrator.results['vision'] = results['vision_analysis'][0]['result']
            if results.get('network_analysis'):
                self.orchestrator.results['network'] = results['network_analysis'][0]['result']
            
            final = self.orchestrator._fuse_results()
        except:
            # Fallback assessment
            final = {
                'threat_level': overall_threat,
                'confidence': 'Medium',
                'summary': f"Analysis complete. Overall threat level: {overall_threat}",
                'recommendations': 'Review individual agent reports for details.'
            }
        
        return final
    
    def save_results(self, results: Dict[str, Any]):
        """Save results to output folder, organized by input file structure"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output subdirectories matching input structure
        output_logs_dir = self.output_dir / "logs"
        output_videos_dir = self.output_dir / "videos"
        output_network_dir = self.output_dir / "network"
        output_logs_dir.mkdir(exist_ok=True)
        output_videos_dir.mkdir(exist_ok=True)
        output_network_dir.mkdir(exist_ok=True)
        
        saved_files = []
        
        # Save individual log analysis results
        for log_result in results.get('log_analysis', []):
            input_filename = Path(log_result['file']).stem
            json_file = output_logs_dir / f"{input_filename}_report_{timestamp}.json"
            txt_file = output_logs_dir / f"{input_filename}_report_{timestamp}.txt"
            
            # Save JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'input_file': log_result['file'],
                    'timestamp': results['timestamp'],
                    'analysis': log_result['result']
                }, f, indent=2, ensure_ascii=False)
            
            # Save TXT
            with open(txt_file, 'w', encoding='utf-8') as f:
                self._write_log_report(f, log_result, results['timestamp'])
            
            saved_files.append((json_file, txt_file))
        
        # Save individual vision analysis results
        for vision_result in results.get('vision_analysis', []):
            input_filename = Path(vision_result['file']).stem
            json_file = output_videos_dir / f"{input_filename}_report_{timestamp}.json"
            txt_file = output_videos_dir / f"{input_filename}_report_{timestamp}.txt"
            
            # Save JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'input_file': vision_result['file'],
                    'timestamp': results['timestamp'],
                    'analysis': vision_result['result']
                }, f, indent=2, ensure_ascii=False)
            
            # Save TXT
            with open(txt_file, 'w', encoding='utf-8') as f:
                self._write_vision_report(f, vision_result, results['timestamp'])
            
            saved_files.append((json_file, txt_file))
        
        # Save individual network analysis results
        for network_result in results.get('network_analysis', []):
            input_filename = Path(network_result['file']).stem if network_result['file'] != 'live_system' else 'live_system'
            json_file = output_network_dir / f"{input_filename}_report_{timestamp}.json"
            txt_file = output_network_dir / f"{input_filename}_report_{timestamp}.txt"
            
            # Save JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'input_file': network_result['file'],
                    'timestamp': results['timestamp'],
                    'analysis': network_result['result']
                }, f, indent=2, ensure_ascii=False)
            
            # Save TXT
            with open(txt_file, 'w', encoding='utf-8') as f:
                self._write_network_report(f, network_result, results['timestamp'])
            
            saved_files.append((json_file, txt_file))
        
        # Save comprehensive report
        comprehensive_json = self.output_dir / f"comprehensive_report_{timestamp}.json"
        comprehensive_txt = self.output_dir / f"comprehensive_report_{timestamp}.txt"
        
        with open(comprehensive_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        with open(comprehensive_txt, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("COMPREHENSIVE CYBERSECURITY THREAT ASSESSMENT REPORT\n")
            f.write("="*60 + "\n\n")
            f.write(f"Generated: {results['timestamp']}\n\n")
            
            # Log Analysis
            if results.get('log_analysis'):
                f.write("LOG ANALYSIS\n")
                f.write("-"*60 + "\n")
                for log_result in results['log_analysis']:
                    f.write(f"File: {log_result['file']}\n")
                    f.write(f"Threat Level: {log_result['result'].get('threat_level', 'UNKNOWN')}\n")
                    f.write(f"Details: {log_result['result'].get('details', 'N/A')}\n")
                    f.write(f"Confidence: {log_result['result'].get('confidence', 0.0)}\n\n")
            
            # Vision Analysis
            if results.get('vision_analysis'):
                f.write("VISION ANALYSIS\n")
                f.write("-"*60 + "\n")
                for vision_result in results['vision_analysis']:
                    f.write(f"File: {vision_result['file']}\n")
                    f.write(f"Threat Level: {vision_result['result'].get('threat_level', 'UNKNOWN')}\n")
                    f.write(f"Details: {vision_result['result'].get('details', 'N/A')}\n")
                    f.write(f"Confidence: {vision_result['result'].get('confidence', 0.0)}\n\n")
            
            # Network Analysis
            if results.get('network_analysis'):
                f.write("NETWORK ANALYSIS\n")
                f.write("-"*60 + "\n")
                for network_result in results['network_analysis']:
                    f.write(f"Source: {network_result['file']}\n")
                    f.write(f"Threat Level: {network_result['result'].get('threat_level', 'UNKNOWN')}\n")
                    f.write(f"Details: {network_result['result'].get('details', 'N/A')}\n")
                    f.write(f"Confidence: {network_result['result'].get('confidence', 0.0)}\n\n")
            
            # Final Assessment
            if results.get('final_assessment'):
                f.write("FINAL ASSESSMENT\n")
                f.write("="*60 + "\n")
                final = results['final_assessment']
                f.write(f"Threat Level: {final.get('threat_level', 'UNKNOWN')}\n")
                f.write(f"Confidence: {final.get('confidence', 'N/A')}\n")
                f.write(f"\nSummary:\n{final.get('summary', 'N/A')}\n")
                f.write(f"\nRecommendations:\n{final.get('recommendations', 'N/A')}\n")
        
        saved_files.append((comprehensive_json, comprehensive_txt))
        
        print(f"\n[OK] Results saved:")
        print(f"\n[Individual Reports] (organized by input type):")
        for json_file, txt_file in saved_files[:-1]:  # Exclude comprehensive report
            print(f"   {json_file.parent.name}/{json_file.name}")
            print(f"   {txt_file.parent.name}/{txt_file.name}")
        print(f"\n[Comprehensive Report]:")
        print(f"   {comprehensive_json.name}")
        print(f"   {comprehensive_txt.name}")
    
    def _write_log_report(self, f, log_result: Dict[str, Any], timestamp: str):
        """Write individual log report"""
        f.write("="*60 + "\n")
        f.write("LOG ANALYSIS REPORT\n")
        f.write("="*60 + "\n\n")
        f.write(f"Input File: {log_result['file']}\n")
        f.write(f"Generated: {timestamp}\n\n")
        result = log_result['result']
        f.write(f"Agent: {result.get('agent', 'LogAgent')}\n")
        f.write(f"Threat Level: {result.get('threat_level', 'UNKNOWN')}\n")
        f.write(f"Confidence: {result.get('confidence', 0.0)}\n")
        f.write(f"Status: {result.get('status', 'UNKNOWN')}\n\n")
        f.write("Details:\n")
        f.write("-"*60 + "\n")
        f.write(f"{result.get('details', 'N/A')}\n")
    
    def _write_vision_report(self, f, vision_result: Dict[str, Any], timestamp: str):
        """Write individual vision report"""
        f.write("="*60 + "\n")
        f.write("VISION ANALYSIS REPORT\n")
        f.write("="*60 + "\n\n")
        f.write(f"Input File: {vision_result['file']}\n")
        f.write(f"Generated: {timestamp}\n\n")
        result = vision_result['result']
        f.write(f"Agent: {result.get('agent', 'VisionAgent')}\n")
        f.write(f"Threat Level: {result.get('threat_level', 'UNKNOWN')}\n")
        f.write(f"Confidence: {result.get('confidence', 0.0)}\n")
        f.write(f"Status: {result.get('status', 'UNKNOWN')}\n\n")
        f.write("Details:\n")
        f.write("-"*60 + "\n")
        f.write(f"{result.get('details', 'N/A')}\n")
    
    def _write_network_report(self, f, network_result: Dict[str, Any], timestamp: str):
        """Write individual network report"""
        f.write("="*60 + "\n")
        f.write("NETWORK ANALYSIS REPORT\n")
        f.write("="*60 + "\n\n")
        f.write(f"Source: {network_result['file']}\n")
        f.write(f"Generated: {timestamp}\n\n")
        result = network_result['result']
        f.write(f"Agent: {result.get('agent', 'NetworkAgent')}\n")
        f.write(f"Threat Level: {result.get('threat_level', 'UNKNOWN')}\n")
        f.write(f"Confidence: {result.get('confidence', 0.0)}\n")
        f.write(f"Status: {result.get('status', 'UNKNOWN')}\n\n")
        f.write("Details:\n")
        f.write("-"*60 + "\n")
        f.write(f"{result.get('details', 'N/A')}\n")
    
    def print_summary(self, results: Dict[str, Any]):
        """Print summary of results"""
        print(f"\n{'='*60}")
        print("PROCESSING COMPLETE - SUMMARY")
        print(f"{'='*60}")
        
        if results.get('final_assessment'):
            final = results['final_assessment']
            threat_level = final.get('threat_level', 'UNKNOWN')
            
            if threat_level == 'CRITICAL':
                icon = '[CRITICAL]'
            elif threat_level == 'WARNING':
                icon = '[WARNING]'
            else:
                icon = '[SECURE]'
            
            print(f"\n{icon} Overall Threat Level: {threat_level}")
            print(f"   Confidence: {final.get('confidence', 'N/A')}")
            print(f"\n   Summary: {final.get('summary', 'N/A')[:200]}...")
            print(f"\n   Recommendations: {final.get('recommendations', 'N/A')[:200]}...")
        
        print(f"\n[Analysis Summary]:")
        print(f"   - Log files analyzed: {len(results.get('log_analysis', []))}")
        print(f"   - Video files analyzed: {len(results.get('vision_analysis', []))}")
        print(f"   - Network analyses: {len(results.get('network_analysis', []))}")
        print(f"\n[Results saved to]:")
        print(f"   - Individual reports: {self.output_dir}/logs/, {self.output_dir}/videos/, {self.output_dir}/network/")
        print(f"   - Comprehensive report: {self.output_dir}/")


def main():
    """Main entry point"""
    processor = InputProcessor()
    processor.process_all()


if __name__ == "__main__":
    main()

