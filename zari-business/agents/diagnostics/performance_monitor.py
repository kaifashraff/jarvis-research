#!/usr/bin/env python3
"""
Performance Monitoring System
JARVIS v2.0 - Real-time Diagnostics
"""

import json
import time
from datetime import datetime, timedelta

class PerformanceMonitor:
    def __init__(self):
        self.system_metrics = {
            'cpu_usage': [],
            'memory_usage': [],
            'response_times': [],
            'error_rates': [],
            'throughput': []
        }
        self.alerts = []
        self.thresholds = {
            'cpu_usage': 80,
            'memory_usage': 85,
            'response_time': 5.0,
            'error_rate': 5.0,
            'throughput': 100
        }
    
    def collect_metric(self, metric_name: str, value: float, source: str = None):
        """Collect system metric"""
        entry = {
            'value': value,
            'source': source,
            'timestamp': datetime.now().isoformat()
        }
        
        if metric_name in self.system_metrics:
            self.system_metrics[metric_name].append(entry)
        
        # Check thresholds
        self.check_thresholds(metric_name, value)
        
        return entry
    
    def check_thresholds(self, metric_name: str, value: float):
        """Check if metric exceeds thresholds"""
        if metric_name in self.thresholds:
            threshold = self.thresholds[metric_name]
            
            if value > threshold:
                alert = {
                    'metric': metric_name,
                    'value': value,
                    'threshold': threshold,
                    'severity': 'critical' if value > threshold * 1.5 else 'warning',
                    'timestamp': datetime.now().isoformat(),
                    'message': f"{metric_name} exceeded threshold: {value} > {threshold}"
                }
                
                self.alerts.append(alert)
                return alert
        
        return None
    
    def get_system_health(self):
        """Get overall system health score"""
        health_scores = []
        
        for metric_name, history in self.system_metrics.items():
            if history:
                recent_value = history[-1]['value']
                threshold = self.thresholds.get(metric_name, 100)
                
                # Calculate health score (0-100)
                if metric_name in ['cpu_usage', 'memory_usage', 'error_rate']:
                    # Lower is better
                    score = max(0, 100 - (recent_value / threshold * 100))
                else:
                    # Higher is better for throughput, lower for response time
                    score = min(100, (recent_value / threshold * 100))
                
                health_scores.append(score)
        
        if health_scores:
            return sum(health_scores) / len(health_scores)
        
        return 0
    
    def get_performance_report(self):
        """Generate performance report"""
        report = {
            'system_health': self.get_system_health(),
            'metrics_summary': {},
            'active_alerts': len([a for a in self.alerts if a['severity'] == 'critical']),
            'total_alerts': len(self.alerts),
            'timestamp': datetime.now().isoformat()
        }
        
        for metric_name, history in self.system_metrics.items():
            if history:
                values = [entry['value'] for entry in history[-10:]]  # Last 10 entries
                
                report['metrics_summary'][metric_name] = {
                    'current': values[-1],
                    'average': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'trend': self.calculate_trend(values)
                }
        
        return report
    
    def calculate_trend(self, values):
        """Calculate trend from values"""
        if len(values) < 2:
            return 'insufficient_data'
        
        if values[-1] > values[-2]:
            return 'increasing'
        elif values[-1] < values[-2]:
            return 'decreasing'
        else:
            return 'stable'
    
    def simulate_monitoring(self, duration_seconds: int = 30):
        """Simulate performance monitoring"""
        print(f"📊 Simulating {duration_seconds} seconds of monitoring...")
        
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            # Simulate metrics
            self.collect_metric('cpu_usage', 45 + (time.time() % 20), 'system')
            self.collect_metric('memory_usage', 60 + (time.time() % 15), 'system')
            self.collect_metric('response_times', 1.5 + (time.time() % 3), 'api')
            self.collect_metric('error_rates', 1.2 + (time.time() % 2), 'system')
            self.collect_metric('throughput', 150 + (time.time() % 50), 'system')
            
            time.sleep(5)
        
        print("✅ Monitoring simulation complete")
        
        return self.get_performance_report()

# Test the system
if __name__ == "__main__":
    print("📊 Performance Monitor - JARVIS v2.0")
    print("=" * 50)
    
    # Initialize
    monitor = PerformanceMonitor()
    
    # Simulate monitoring
    report = monitor.simulate_monitoring(10)  # 10 seconds
    
    print("\n📈 Performance Report:")
    print(f"System Health: {report['system_health']:.1f}%")
    print(f"Active Alerts: {report['active_alerts']}")
    
    print("\n📊 Metrics Summary:")
    for metric, data in report['metrics_summary'].items():
        print(f"{metric}: {data['current']:.1f} ({data['trend']})")
