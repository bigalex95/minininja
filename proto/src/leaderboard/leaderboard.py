"""
Leaderboard management with Supabase backend
"""
import os
from typing import List, Dict, Optional
from datetime import datetime
from supabase import create_client, Client


class Leaderboard:
    """Manages game leaderboard with Supabase backend"""
    
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Supabase credentials not found. "
                "Please set SUPABASE_URL and SUPABASE_KEY environment variables."
            )
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        self.table_name = 'leaderboard'
    
    def submit_score(self, player_name: str, score: int, difficulty: str = 'medium') -> bool:
        """
        Submit a score to the leaderboard
        
        Args:
            player_name: Name of the player
            score: Score achieved
            difficulty: Game difficulty level
            
        Returns:
            True if submission was successful, False otherwise
        """
        try:
            data = {
                'player_name': player_name,
                'score': score,
                'difficulty': difficulty,
                'created_at': datetime.utcnow().isoformat()
            }
            
            response = self.client.table(self.table_name).insert(data).execute()
            if hasattr(response, 'error') and response.error:
                print(f"Error submitting score: {response.error}")
                return False
            return True
        except Exception as e:
            print(f"Error submitting score: {e}")
            return False
    
    def get_top_scores(self, limit: int = 10, difficulty: Optional[str] = None) -> List[Dict]:
        """
        Get top scores from the leaderboard
        
        Args:
            limit: Maximum number of scores to return
            difficulty: Filter by difficulty level (None for all)
            
        Returns:
            List of score entries
        """
        try:
            query = self.client.table(self.table_name).select('*')
            
            if difficulty:
                query = query.eq('difficulty', difficulty)
            
            response = query.order('score', desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching leaderboard: {e}")
            return []
    
    def get_player_rank(self, player_name: str, difficulty: Optional[str] = None) -> Optional[int]:
        """
        Get the rank of a specific player
        
        Args:
            player_name: Name of the player
            difficulty: Filter by difficulty level
            
        Returns:
            Player's rank (1-indexed) or None if not found
        """
        try:
            query = self.client.table(self.table_name).select('player_name, score')
            
            if difficulty:
                query = query.eq('difficulty', difficulty)
            
            response = query.order('score', desc=True).execute()
            
            for idx, entry in enumerate(response.data, 1):
                if entry['player_name'] == player_name:
                    return idx
            
            return None
        except Exception as e:
            print(f"Error getting player rank: {e}")
            return None
    
    def get_player_best_score(self, player_name: str, difficulty: Optional[str] = None) -> Optional[int]:
        """
        Get the best score for a specific player
        
        Args:
            player_name: Name of the player
            difficulty: Filter by difficulty level
            
        Returns:
            Best score or None if not found
        """
        try:
            query = self.client.table(self.table_name).select('score')
            query = query.eq('player_name', player_name)
            
            if difficulty:
                query = query.eq('difficulty', difficulty)
            
            response = query.order('score', desc=True).limit(1).execute()
            
            if response.data:
                return response.data[0]['score']
            return None
        except Exception as e:
            print(f"Error getting player best score: {e}")
            return None
