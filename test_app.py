import unittest
from urllib import response
from myapp import app   # myapp 모듈(파이썬 코드)에서 플라스크 애플리케이션을 가져옵니다.

# BasicTestCase 클래스는 unittest.TestCase를 상속받습니다.
class BasicTestCase(unittest.TestCase):

    # index 라우트를 테스트하는 메서드입니다.
    def test_index(self):
        # 플라스크 애프리케이션을 위한 테스트 클라이언트 인스턴스를 생성합니다.
        tester = app.test_client(self)
        # 테스트 클라이언트를 사용하여 루트 URL로 GET 요청을 보냅니다.
        response = tester.get('/', content_type='html/text')
        # 응답다은 상태 코드가 200인지 확인합니다.
        self.assertEqual(response.status_code, 200)

# AdvancedTestCase 클래스는 unittest.TestCase를 상속받습니다.
class AdvancedTestCase(unittest.TestCase):
    
    def setUp(self):
        # 플라스크 애프리케이션을 위한 테스트 클라이언트 인스턴스를 생성합니다.
        self.tester = app.test_client(self)

    def tearDown(self):
        # 테스트가 끝난 후 정리 작업을 수행합니다. 현재는 비어있는 상태입니다.
        pass

    # index 라우트를 테스트하는 메서드입니다.
    def test_index(self):
        # 테스트 클라이언트를 사용하여 루트 URL로 GET 요청을 보냅니다.
        response = self.tester.get('/', content_type='html/text')
        # 응답다은 상태 코드가 200인지 확인합니다.
        self.assertEqual(response.status_code, 200)

    # test_index_text 메서드는 루트 경로의 응답 텍스트를 테스트합니다.
    def test_index_text(self):
        # 루트 경로에 GET 요청을 보내고 응답 데이터를 검증합니다.
        response = self.tester.get('/', content_type='html/text')
        # 응답 데이터가 'Hello World!'와 일치하는지 바이트 문자열로 확인합니다.
        self.assertEqual(response.data, b'Hello World!')

    # test_another_route(self):
    def test_another_route(self):
        # '/another' 경로에 GET 요청을 보내고 상태 코드를 검증합니다.
        response = self.tester.get('/another', content_type = 'html/text')
        # 해당 경로에 존재하지 않으므로 상태 코드가 404(찾을 수 없음)인지 확인합니다.
        self.assertEqual(response.status_code, 404)
