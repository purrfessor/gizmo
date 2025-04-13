"""
Metrics utilities for Gizmo.

This module provides utilities for tracking and accumulating usage metrics
from agno RunResponse objects.
"""
from typing import Dict, Any


class UsageAccumulator:
    """
    A class for accumulating usage metrics from agno RunResponse objects.
    
    This class tracks metrics such as total tokens used and model time
    across multiple RunResponse objects.
    """
    
    def __init__(self):
        """
        Initialize a new UsageAccumulator with zero metrics.
        """
        self.overall_metrics = {
            'total_tokens': 0,
            'model_time': 0
        }
    
    def record(self, response):
        """
        Record metrics from an agno RunResponse object.
        
        Args:
            response: An agno RunResponse object containing metrics to record.
        """
        if response.metrics:
            metrics = response.metrics
            if 'total_tokens' in metrics and metrics['total_tokens']:
                self.overall_metrics['total_tokens'] += metrics['total_tokens'][0]
            if 'time' in metrics and metrics['time']:
                self.overall_metrics['model_time'] += metrics['time'][0]
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get the accumulated metrics.
        
        Returns:
            Dict[str, Any]: A dictionary containing the accumulated metrics.
        """
        return self.overall_metrics
    
    def reset(self):
        """
        Reset all accumulated metrics to zero.
        """
        self.overall_metrics = {
            'total_tokens': 0,
            'model_time': 0
        }