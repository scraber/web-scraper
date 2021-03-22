from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from models.image import PageImage
from tools.scrape import get_all_images_data

class PageImageView(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url', type=str, required=True, help="URL required!")

    def get(self):
        data = PageImageView.parser.parse_args()
        return PageImage.find_url(data['url']).to_json()

    def post(self):
        data = PageImageView.parser.parse_args()
        if PageImage.query.filter_by(url=data['url']).first():
            # 409 -> Conflict, already exists
            return {'message': f"This url '{data['url']}' was already scrapped. If you want to update this resource, please send PUT request."}, 409

        page = PageImage(url=data['url'])
        page.image = get_all_images_data(data['url'])

        try:
            page.save_to_db()
        except SQLAlchemyError:
            # 500 -> Server, transaction error
            return {"message": "An error occurred during save."}, 500

        # 201 -> Created
        return {"message": f"URL's {page.url} images scrapped and saved to DB."}, 201

class PageImageListView(Resource):
    def get(self):
        return [entry.to_json() for entry in PageImage.query.all()]