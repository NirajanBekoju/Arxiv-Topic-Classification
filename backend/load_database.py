import os
from tqdm import tqdm
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arxiv.settings")
django.setup()

import csv
from recommender.models import Arxiv  

def import_data_from_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in tqdm(reader):
            Arxiv.objects.create(
                paper_id = row["id"],
                submitter = row["submitter"],
                author = row["authors"],
                title = row["title"],
                comments = row["comments"],
                doi = row["doi"],
                abstract = row["abstract"],
                date = row["date"],
                categories = row["categories"],
            )
            print(f"Added data from row: {row}")

if __name__ == '__main__':
    csv_file_path = 'model/recommender/original_first_1_million.csv' 
    import_data_from_csv(csv_file_path)