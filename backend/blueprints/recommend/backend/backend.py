####测试用

from model import VideoRecommender, ExerciseRecommender
import json
import os
video_recommender = VideoRecommender()
exercises_recommender = ExerciseRecommender()
test_user_for_video = "U_10000"
test_user_for_exercise = "U_22"
needed_video_num =10
top_k =2*needed_video_num
rec_videos, rec_scores = video_recommender.recommend(test_user_for_video, top_k=top_k)
rec_exercises, rec_scores = exercises_recommender.recommend(test_user_for_exercise, top_k=top_k)

video_ccid_map={}
# 读取视频ID与CCID的映射
try:
    with open(os.path.join('resources','video_id-ccid.txt'), 'r',encoding='utf-8') as f:
        for line in f:
            (key, val) = line.split()
            video_ccid_map[key] = val
except FileNotFoundError:
    print("File not found")

#  将视频id和ccid进行映射
recommended_video_ccids = {}
for video_id in rec_videos:
    if len(recommended_video_ccids) >= needed_video_num:
        break
    if video_id in video_ccid_map:
        recommended_video_ccids[video_id] = video_ccid_map[video_id]
    else:
        continue

#将推荐结果里的pm_id与exercise_id进行映射
pm_id_exercise_id_map={}
try:
    with open(os.path.join('resources','exercise-problem.txt'), 'r',encoding='utf-8') as f:
        for line in f:
            (val,key) = line.split()
            pm_id_exercise_id_map[key] = val
except FileNotFoundError:
    print("File not found")

recommended_exercise_id=[]
for exercise_id in rec_exercises:
    if len(recommended_exercise_id) >= needed_video_num:
        break
    if exercise_id in pm_id_exercise_id_map:
        recommended_exercise_id.append(pm_id_exercise_id_map[exercise_id])
    else:
        continue

print(recommended_exercise_id)
#将习题id与题目数据进行映射
#将json缓存在字典里加快查找
exercise_json_map={}
try:
    with open(os.path.join('resources','exercise-problem.txt'), 'r',encoding='utf-8') as f:
        content = f.read()
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                if 'exercise_id' in item:
                    exercise_json_map[item['exercise_id']] = json.dumps(item)
            except json.JSONDecodeError:
                print(f"无法解析JSON行: {line[:50]}...")
except FileNotFoundError:
    print("File not found")
print(len(exercise_json_map))
#  将习题id和题目数据进行映射
recommended_exercise_data = {}
for exercise_id in recommended_exercise_id:
    if len(recommended_exercise_data) >= needed_video_num:
        break
    if exercise_id in exercise_json_map:
        recommended_exercise_data[exercise_id] = exercise_json_map[exercise_id]
    else:
        continue


print("推荐视频的ccid映射:")
for video_id, ccid in recommended_video_ccids.items():
    print(f"视频ID: {video_id}, CCID: {ccid}")
print("推荐习题的数据:")
for exercise_id, data in recommended_exercise_data.items():
    print(f"习题ID: {exercise_id}, 数据: {data}")
    print(type(data))
