from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from models.text import PageText


class PageTextView(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url', type=str, required=True, help="URL required!")

    def get(self):
        data = PageTextView.parser.parse_args()
        return PageText.find_url_or_404(data['url']).to_json()

    def post(self):
        data = PageTextView.parser.parse_args()
        if PageText.query.filter_by(url=data['url']).first():
            # 409 -> Conflict, already exists
            return {'message': f"This url '{data['url']}' was already scrapped. If you want to update this resource, please send PUT request."}, 409

        page = PageText(url=data['url'])

        try:
            page.save_to_db()
        except SQLAlchemyError:
            # 500 -> Server, transaction error
            return {"message": "An error occurred during save."}, 500 

        # 201 -> Created
        return {"message": f"URL's {page.url} text scrapped and saved to DB."}, 201

class PageTextListView(Resource):
    def get(self):
        return [entry.to_json() for entry in PageText.query.all()]