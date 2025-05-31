import os
import torch
import pickle
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 获取当前文件所在的目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_DIR)))  # 回退到lastproject2目录

# 基于BASE_DIR构建路径
MODEL_PATH = os.path.join(CURRENT_DIR, "..", "..", "models", "model_video.pt")
EMBEDDING_PATH = os.path.join(CURRENT_DIR, "..", "..", "models", "node_embeddings_video.pt")
USER2IDX_PATH = os.path.join(CURRENT_DIR, "..", "..", "models", "user2idx.pkl")
VIDEO2IDX_PATH = os.path.join(CURRENT_DIR, "..", "..", "models", "video2idx.pkl")

MODEL_PATH_EX = os.path.join(CURRENT_DIR, "..", "..", "models", "ktm_lc_model.pt")
EMBEDDING_PATH_EX = os.path.join(CURRENT_DIR, "..", "..", "models", "node_embeddings_exercises.pt")
USER2IDX_PATH_EX = os.path.join(CURRENT_DIR, "..", "..", "models", "user2idx_ex.pkl")
PROBLEM2IDX_PATH_EX = os.path.join(CURRENT_DIR, "..", "..", "models", "problem2idx.pkl")


class VideoRecommender:
    def __init__(self, model_path=MODEL_PATH, embedding_path=EMBEDDING_PATH,
                 user2idx_path=USER2IDX_PATH, video2idx_path=VIDEO2IDX_PATH):
        self.model_path = model_path
        self.embedding_path = embedding_path
        self.user2idx, self.video2idx, self.idx2video = self.load_mappings(user2idx_path, video2idx_path)
        self.embeddings = self.load_embeddings()

    def load_mappings(self, user2idx_path, video2idx_path):
        try:
            with open(user2idx_path, "rb") as f:
                user2idx = pickle.load(f)
            with open(video2idx_path, "rb") as f:
                video2idx = pickle.load(f)
            idx2video = {idx: vid for vid, idx in video2idx.items()}
            return user2idx, video2idx, idx2video
        except FileNotFoundError as e:
            print(f"找不到文件: {str(e)}")
            print(f"尝试查找的路径: {os.path.abspath(user2idx_path)}")
            print(f"当前工作目录: {os.getcwd()}")
            raise

    def load_embeddings(self):
        try:
            embeddings = torch.load(self.embedding_path, map_location=device)
            return embeddings
        except FileNotFoundError as e:
            print(f"找不到嵌入文件: {str(e)}")
            print(f"尝试查找的路径: {os.path.abspath(self.embedding_path)}")
            raise

    def recommend(self, user_id, top_k=20):
        if user_id not in self.user2idx:
            raise ValueError(f"未知的 user_id: {user_id}")
        num_users = len(self.user2idx)
        u_idx = self.user2idx[user_id]
        user_emb = self.embeddings[u_idx]
        video_embs = self.embeddings[num_users: num_users + len(self.video2idx)]

        scores = torch.matmul(video_embs, user_emb)
        scores_np = scores.cpu().numpy()

        top_indices = np.argsort(-scores_np)[:top_k]
        recommended_videos = [self.idx2video[idx] for idx in top_indices]
        if(len(recommended_videos) >= top_k//2):
            return recommended_videos[:top_k//2], scores_np[top_indices[:top_k//2]]
        else:
            return recommended_videos, scores_np[top_indices]

class ExerciseRecommender:
    def __init__(self, model_path=MODEL_PATH_EX, embedding_path=EMBEDDING_PATH_EX,
                 user2idx_path=USER2IDX_PATH_EX, problem2idx_path=PROBLEM2IDX_PATH_EX):
        self.model_path = model_path
        self.embedding_path = embedding_path
        self.user2idx, self.problem2idx, self.idx2problem = self.load_mappings(user2idx_path, problem2idx_path)
        self.embeddings = self.load_embeddings()

    def load_mappings(self, user2idx_path, problem2idx_path):
        try:
            with open(user2idx_path, "rb") as f:
                user2idx = pickle.load(f)
            with open(problem2idx_path, "rb") as f:
                problem2idx = pickle.load(f)
            # 构建反向映射：索引到习题ID
            idx2problem = {idx: pid for pid, idx in problem2idx.items()}
            return user2idx, problem2idx, idx2problem
        except FileNotFoundError as e:
            print(f"找不到文件: {str(e)}")
            print(f"尝试查找的路径: {os.path.abspath(user2idx_path)}")
            print(f"当前工作目录: {os.getcwd()}")
            raise

    def load_embeddings(self):
        try:
            # 加载训练好的习题推荐模型的节点嵌入
            embeddings = torch.load(self.embedding_path, map_location=device)
            return embeddings
        except FileNotFoundError as e:
            print(f"找不到嵌入文件: {str(e)}")
            print(f"尝试查找的路径: {os.path.abspath(self.embedding_path)}")
            raise

    def recommend(self, user_id, top_k=20):
        """
        根据给定 user_id 推荐 top_k 个习题。
        模型假设：节点顺序为前 num_users 个为用户节点，
        后续为习题节点，习题数 = len(problem2idx)。
        返回推荐的习题ID列表及对应的匹配得分。
        """
        if user_id not in self.user2idx:
            raise ValueError(f"未知的 user_id: {user_id}")
        num_users = len(self.user2idx)
        u_idx = self.user2idx[user_id]
        # 用户嵌入向量
        user_emb = self.embeddings[u_idx]
        # 习题节点嵌入：假设习题节点从索引 num_users 开始
        exercise_embs = self.embeddings[num_users: num_users + len(self.problem2idx)]
        # 计算内积得分
        scores = torch.matmul(exercise_embs, user_emb)
        scores_np = scores.cpu().numpy()
        # 取得分最高的 top_k 个习题索引
        top_indices = np.argsort(-scores_np)[:top_k]
        recommended_exercises = [self.idx2problem[idx] for idx in top_indices]
        if(len(recommended_exercises) > top_k//2):
            return recommended_exercises[:top_k//2], scores_np[top_indices[:top_k//2]]
        else:
            return recommended_exercises, scores_np[top_indices]

if __name__ == "__main__":
    """
    其他文件可以直接调用 VideoRecommender 类，输入用户 ID，返回推荐的视频 ID 和对应的分数。
    """
    video_recommender = VideoRecommender()
    exercises_recommender = ExerciseRecommender()
    test_user_for_video = "U_10000"
    test_user_for_exercise = "U_22"
    top_k = 10
    rec_videos, rec_scores = video_recommender.recommend(test_user_for_video, top_k=top_k)
    rec_exercises, rec_scores = exercises_recommender.recommend(test_user_for_exercise, top_k=top_k)
    print(rec_videos)
    print(rec_exercises)
