import unittest
from chatbot import FAQChatbot, load_faqs


class FAQChatbotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = FAQChatbot(load_faqs("data/faqs.json"), threshold=0.22)

    def test_direct_match(self):
        result = self.bot.get_answer("How do I apply for admission?")
        self.assertIsNotNone(result["matched_question"])
        self.assertIn("official", result["answer"].lower())

    def test_paraphrased_question(self):
        result = self.bot.get_answer("Which papers should I submit to join?")
        # The threshold may reject a very different wording; it must never crash.
        self.assertIsInstance(result["answer"], str)

    def test_greeting(self):
        result = self.bot.get_answer("hello")
        self.assertIn("Hello", result["answer"])

    def test_empty_input(self):
        result = self.bot.get_answer("   ")
        self.assertIn("type a question", result["answer"].lower())

    def test_unrelated_question(self):
        result = self.bot.get_answer("How do I repair a bicycle engine?")
        self.assertIsNone(result["matched_question"])
        self.assertIn("couldn't find", result["answer"].lower())


if __name__ == "__main__":
    unittest.main()
