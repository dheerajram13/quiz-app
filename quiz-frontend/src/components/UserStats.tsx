import React, { useEffect, useState } from 'react';
import api from '../services/api';

interface UserStatsData {
    total_quizzes: number;
    average_score: number;
    highest_score: number;
}

const UserStats: React.FC = () => {
    const [stats, setStats] = useState<UserStatsData | null>(null);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await api.get('/quizzes/user_stats/');
                setStats(response.data as UserStatsData);
            } catch (error) {
                console.error("Error fetching user stats:", error);
            }
        };

        fetchStats();
    }, []);

    return (
        <div>
            <h2>User Stats</h2>
            {stats ? (
                <div>
                    <p>Total Quizzes Taken: {stats.total_quizzes}</p>
                    <p>Average Score: {stats.average_score}</p>
                    <p>Highest Score: {stats.highest_score}</p>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default UserStats;
