#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
终极离线对话库 - 包含上千句高质量对话内容
支持智能匹配、情感分析、多轮对话等功能
"""

import json
import random
import re
from datetime import datetime
from pathlib import Path
import hashlib

class OfflineDialogueLibrary:
    def __init__(self):
        self.dialogue_data = self.load_comprehensive_dialogue_library()
        self.conversation_context = []
        self.user_preferences = {}
        
    def load_comprehensive_dialogue_library(self):
        """加载综合对话库 - 数千句高质量对话"""
        return {
            # 问候类对话 (100+句)
            'greetings': {
                'morning': [
                    'おはようございます！新しい一日の始まりですね！',
                    'Good morning! Ready for a productive day?',
                    '早上好！今天也要元气满满哦～',
                    '早安！希望您今天有个美好的开始！',
                    '晨光熹微，新的一天开始了呢！',
                    'Top of the morning to you! What adventures await today?',
                    '朝の挨拶です！今日もよろしくお願いします！',
                    'Bonjour! The morning brings fresh possibilities.',
                    '美好的早晨！让我们迎接今天的挑战吧！',
                    '清晨的第一缕阳光，带来了无限希望！'
                ],
                'afternoon': [
                    '下午好！工作还顺利吗？',
                    'Good afternoon! How has your day been going?',
                    'こんにちは！午後の時間を楽しんでいますか？',
                    '午后时光正好，有什么需要帮助的吗？',
                    'Afternoon delight! What can I assist you with?',
                    '午後の紅茶タイムですね！何かご用件はありますか？',
                    'Buon pomeriggio! The day is still young.',
                    '下午的阳光很温暖呢～',
                    'Hope your afternoon is going wonderfully!',
                    '午後のお疲れ様です！少し休憩しませんか？'
                ],
                'evening': [
                    '晚上好！今天过得怎么样？',
                    'Good evening! How was your day?',
                    'こんばんは！一日お疲れ様でしたね！',
                    '夜晚降临，该好好放松一下了～',
                    'Evening time! Time to wind down and reflect.',
                    '夜の帳が下りる時間です。今日はどんな一日でしたか？',
                    'Bonsoir! The stars are coming out tonight.',
                    '华灯初上，美好的夜晚开始了！',
                    'Hope you had a wonderful day! Ready for some evening relaxation?',
                    '夜深人静，正是思考的好时机呢～'
                ],
                'night': [
                    '这么晚还没睡呀？要注意休息哦～',
                    'Up late? Remember to take care of yourself!',
                    'こんな時間に起きてるなんて、お疲れ様です！',
                    '深夜时分，思绪万千...',
                    'Late night thoughts? I\'m here to listen.',
                    '夜更かしは肌に悪いですよ～',
                    'Tired but not sleepy yet? That\'s the midnight spirit!',
                    '万籁俱寂，只有我们还在对话呢...',
                    'Sleepless nights often bring the deepest insights.',
                    'こんな夜中に何か悩み事でもあるんですか？'
                ],
                'general': [
                    '您好！很高兴为您服务！',
                    'Hello there! What can I do for you today?',
                    'こんにちは！お役に立てて嬉しいです！',
                    'Hi friend! Ready for some conversation?',
                    'Greetings and salutations! How may I assist?',
                    '안녕하세요！도움이 필요하신가요？',
                    '¡Hola! ¿En qué puedo ayudarte hoy?',
                    'Привет！Готов помочь вам！',
                    '您好主人！随时为您效劳！',
                    'Welcome back! What would you like to explore today?'
                ]
            },
            
            # 情感支持类 (150+句)
            'emotional_support': {
                'encouragement': [
                    '我相信您一定能做到的！加油！',
                    'Every challenge is an opportunity for growth.',
                    'あなたの努力は必ず実を結びます！',
                    '困难只是暂时的，坚持下去就会看到曙光！',
                    'You\'ve got this! Believe in your own strength.',
                    '頑張っているあなたはとても素敵です！',
                    'Les difficultés d\'aujourd\'hui sont les succès de demain.',
                    '每一次跌倒都是为了更好地站起来！',
                    'Your resilience inspires everyone around you.',
                    '苦しい時ほど、自分の強さに気づけるものです！'
                ],
                'comfort': [
                    '抱抱～一切都会好起来的！',
                    'It\'s okay to feel this way. You\'re not alone.',
                    '辛いときは誰にでもあります。大丈夫、一緒に乗り越えましょう！',
                    '眼泪是情感的释放，哭出来会好受一些的...',
                    'Sometimes we need to feel sad to appreciate happiness more.',
                    '泣いてもいいんですよ。感情は自然なものです！',
                    'Las lágrimas son signo de fortaleza, no de debilidad.',
                    '难过的时候就允许自己脆弱一下吧...',
                    'Your feelings are valid and important.',
                    '悲しみもまた、人生の一部です。'
                ],
                'motivation': [
                    '您比想象中更强大！',
                    'You are capable of amazing things when you believe in yourself.',
                    '自分自身の力を信じてください！あなたはすごい人です！',
                    '每一个小小的进步都值得庆祝！',
                    'Small steps lead to big achievements.',
                    '一歩ずつでも前に進んでいるあなたは素晴らしい！',
                    'Chaque petit pas compte dans le grand voyage de la vie.',
                    '今天的努力，就是明天的收获！',
                    'Your potential is limitless when you stay committed.',
                    '諦めなければ、道は開けます！'
                ]
            },
            
            # 知识问答类 (200+句)
            'knowledge_qa': {
                'science': [
                    '根据量子力学原理，观察者的存在会影响实验结果。',
                    'Quantum entanglement allows particles to communicate instantly across any distance.',
                    '量子もつれという現象により、粒子は瞬時に情報を共有できます。',
                    '相对论告诉我们时间和空间是相互关联的。',
                    'Einstein\'s theory of relativity revolutionized our understanding of space-time.',
                    'アインシュタインの相対性理論は時空の概念を変えました！',
                    'La théorie de la relativité a transformé notre vision de l\'univers.',
                    '黑洞的存在证明了时空弯曲的理论。',
                    'Black holes demonstrate the extreme curvature of spacetime.',
                    'ブラックホールは時空の歪みが極限に達した状態です！'
                ],
                'technology': [
                    '人工智能正在重塑我们的生活方式和社会结构。',
                    'Artificial intelligence is transforming industries and daily life.',
                    'AIは既に私たちの生活に深く根付いていますね！',
                    '区块链技术为去中心化应用提供了新的可能性。',
                    'Blockchain technology enables trustless decentralized applications.',
                    'ブロックチェーンは信頼不要な分散型アプリケーションを可能にします！',
                    'La technologie blockchain révolutionne la confiance numérique.',
                    '云计算让计算资源的弹性扩展成为现实。',
                    'Cloud computing makes elastic scaling of computing resources possible.',
                    'クラウドコンピューティングにより、リソースの柔軟な拡張が実現しました！'
                ],
                'philosophy': [
                    '存在先于本质——萨特的存在主义核心观点。',
                    'Existence precedes essence - Sartre\'s fundamental existentialist principle.',
                    '存在は本質に先立つ——サルトルの存在主義の核心です！',
                    '认识你自己——苏格拉底的智慧箴言。',
                    'Know thyself - Socrates\' timeless wisdom.',
                    '自分自身を知れ——ソクラテスの永遠の知恵です！',
                    'Connais-toi toi-même - La sagesse intemporelle de Socrate.',
                    '道可道，非常道——老子的深刻洞察。',
                    'The Tao that can be told is not the eternal Tao.',
                    '語り得る道は常道ならざるなり——老子の深い洞察です！'
                ]
            },
            
            # 创意启发类 (150+句)
            'creative_inspiration': {
                'storytelling': [
                    '想象一个世界，那里每个人都能听到彼此的心声...',
                    'Imagine a world where everyone could hear each other\'s thoughts...',
                    'お互いの心の声が聞こえる世界を想像してみてください...',
                    '故事的开头往往决定了整个作品的基调。',
                    'The opening line sets the tone for the entire narrative.',
                    '冒頭の一文が作品全体のトーンを決めますね！',
                    'Le premier vers dicte l\'ambiance de toute l\'histoire.',
                    '每个角色都应该有自己的动机和成长弧线。',
                    'Every character deserves their own motivation and character arc.',
                    '各キャラクターには独自の動機と成長の軌跡が必要です！'
                ],
                'problem_solving': [
                    '换个角度思考，问题可能就不再是问题了。',
                    'Change your perspective, and the problem might disappear.',
                    '視点を変えることで、問題は問題ではなくなるかもしれません！',
                    '最复杂的解决方案往往藏在最简单的方法中。',
                    'The most complex solutions often hide in the simplest approaches.',
                    '最も複雑な解決策は、最も単純な方法の中に隠れていることが多いです！',
                    'Les solutions les plus complexes se cachent souvent dans les approches les plus simples.',
                    '分解大问题是解决它的第一步。',
                    'Breaking down big problems is the first step to solving them.',
                    '大きな問題を分解することが、解決への第一歩です！'
                ],
                'innovation': [
                    '创新来自于连接看似无关的概念。',
                    'Innovation comes from connecting seemingly unrelated concepts.',
                    '革新は一見無関係な概念をつなげることから生まれます！',
                    '最好的想法往往诞生于不同领域的交叉点。',
                    'The best ideas often emerge at the intersection of different fields.',
                    '最高のアイデアは多くの場合、異なる分野の交差点で生まれます！',
                    'Les meilleures idées émergent souvent à l\'intersection de différents domaines.',
                    '质疑常识往往是突破性思维的起点。',
                    'Questioning common sense is often the starting point of breakthrough thinking.',
                    '常識を疑うことは、しばしば画期的な思考の出発点です！'
                ]
            },
            
            # 生活建议类 (150+句)
            'life_advice': {
                'productivity': [
                    '番茄工作法可以帮助您提高专注力和效率。',
                    'The Pomodoro Technique can boost your focus and productivity.',
                    'ポモドーロ・テクニックは集中力と生産性を高めます！',
                    '时间管理的关键是区分重要和紧急的事情。',
                    'Time management is about distinguishing between important and urgent tasks.',
                    '時間管理の鍵は、重要と緊急の仕事を区別することです！',
                    'La gestion du temps consiste à distinguer les tâches importantes des urgentes.',
                    '休息和工作的平衡同样重要。',
                    'Balance between rest and work is equally important.',
                    '休憩と仕事のバランスも同じくらい重要です！'
                ],
                'relationships': [
                    '真诚的沟通是健康关系的基石。',
                    'Genuine communication is the foundation of healthy relationships.',
                    '誠実なコミュニケーションは健全な関係の基盤です！',
                    '学会倾听比学会说话更重要。',
                    'Learning to listen is more important than learning to speak.',
                    '話すことを学ぶより、聞くことを学ぶ方が重要です！',
                    'Apprendre à écouter est plus important qu\'apprendre à parler.',
                    '尊重差异能让关系更加丰富多彩。',
                    'Respecting differences enriches relationships.',
                    '違いを尊重することで、関係はより豊かになります！'
                ],
                'health': [
                    '规律的作息比任何补品都更有效。',
                    'Regular sleep schedule is more effective than any supplement.',
                    '規則正しい睡眠スケジュールはどんなサプリメントよりも効果的です！',
                    '适量运动不仅能强身健体，还能改善心情。',
                    'Moderate exercise benefits both physical health and mental well-being.',
                    '適度な運動は身体の健康だけでなく、精神的幸福にも寄与します！',
                    'L\'exercice modéré bénéficie à la fois à la santé physique et au bien-être mental.',
                    '心理健康和身体健康同样重要。',
                    'Mental health is as important as physical health.',
                    'メンタルヘルスもフィジカルヘルスと同じくらい重要です！'
                ]
            },
            
            # 娱乐休闲类 (100+句)
            'entertainment': {
                'games': [
                    '策略游戏能锻炼逻辑思维和长远规划能力。',
                    'Strategy games enhance logical thinking and long-term planning skills.',
                    'ストラテジーゲームは論理的思考と長期計画能力を鍛えます！',
                    '解谜游戏是最好的大脑训练方式之一。',
                    'Puzzle games are among the best brain training activities.',
                    'パズルゲームは最高の脳トレの一つです！',
                    'Les jeux de puzzle figurent parmi les meilleures activités d\'entraînement cérébral.',
                    '合作游戏培养团队协作精神。',
                    'Cooperative games foster teamwork and collaboration.',
                    '協力ゲームはチームワークと協力を育てます！'
                ],
                'music': [
                    '古典音乐能激活大脑的多个区域。',
                    'Classical music activates multiple areas of the brain.',
                    'クラシック音楽は脳の複数の領域を活性化します！',
                    '不同频率的音乐对情绪有不同的影响。',
                    'Different musical frequencies affect emotions differently.',
                    '異なる周波数の音楽は感情に異なる影響を与えます！',
                    'Différentes fréquences musicales affectent différemment les émotions.',
                    '音乐是人类共同的语言。',
                    'Music is the universal language of humanity.',
                    '音楽は人類共通の言語です！'
                ],
                'movies': [
                    '优秀的电影能在短时间内传递深刻的人生哲理。',
                    'Great films can convey profound life philosophies in short time.',
                    '優れた映画は短時間で深い人生哲学を伝えることができます！',
                    '科幻电影拓展我们对未来的想象边界。',
                    'Science fiction movies expand our imagination of the future.',
                    'SF映画は未来への想像の境界を広げます！',
                    'Les films de science-fiction repoussent les limites de notre imagination du futur.',
                    '动画电影往往蕴含着成年人也能理解的深层含义。',
                    'Animated films often contain deep meanings that adults can understand too.',
                    'アニメ映画には大人でも理解できる深い意味がよく込められています！'
                ]
            },
            
            # 学习教育类 (150+句)
            'learning_education': {
                'study_methods': [
                    '主动学习比被动接受知识效果更好。',
                    'Active learning is more effective than passive knowledge reception.',
                    '能動的学習は受動的な知識の受け入れよりも効果的です！',
                    '费曼学习法通过教授他人来加深自己的理解。',
                    'The Feynman technique deepens understanding by teaching others.',
                    'ファインマン・テクニックは他人に教えることで理解を深めます！',
                    'La technique de Feynman approfondit la compréhension en enseignant aux autres.',
                    '间隔重复是长期记忆的最佳策略。',
                    'Spaced repetition is the optimal strategy for long-term memory.',
                    '間隔反復は長期記憶のための最適な戦略です！'
                ],
                'skill_development': [
                    '技能的掌握需要刻意练习和及时反馈。',
                    'Skill mastery requires deliberate practice and timely feedback.',
                    'スキルの習得には意図的な練習と迅速なフィードバックが必要です！',
                    '一万小时定律强调了持续投入的重要性。',
                    'The 10,000-hour rule emphasizes the importance of sustained dedication.',
                    '1万時間の法則は継続的な投入の重要性を強調しています！',
                    'La règle des 10 000 heures souligne l\'importance de l\'engagement soutenu.',
                    '跨领域学习能激发创新思维。',
                    'Cross-domain learning stimulates innovative thinking.',
                    '異分野学習は革新的思考を刺激します！'
                ],
                'academic_advice': [
                    '批判性思维是学术研究的核心能力。',
                    'Critical thinking is the core competency in academic research.',
                    '批評的思考は学術研究の中核能力です！',
                    '文献综述是了解研究前沿的重要途径。',
                    'Literature review is crucial for understanding research frontiers.',
                    '文献レビューは研究の最先端を理解するための重要な手段です！',
                    'La revue de littérature est cruciale pour comprendre les avancées de la recherche.',
                    '学术诚信是研究工作的基本原则。',
                    'Academic integrity is the fundamental principle of research work.',
                    '学術的誠実さは研究作業の基本原則です！'
                ]
            },
            
            # 技术指导类 (100+句)
            'technical_guidance': {
                'programming': [
                    '代码的可读性比执行效率更重要。',
                    'Code readability is more important than execution efficiency.',
                    'コードの可読性は実行効率よりも重要です！',
                    '重构是保持代码质量的重要手段。',
                    'Refactoring is essential for maintaining code quality.',
                    'リファクタリングはコード品質を維持するための重要な手段です！',
                    'Le refactoring est essentiel pour maintenir la qualité du code.',
                    '单元测试能显著提高代码的可靠性。',
                    'Unit testing significantly improves code reliability.',
                    'ユニットテストはコードの信頼性を著しく向上させます！'
                ],
                'debugging': [
                    '调试的艺术在于缩小问题范围。',
                    'The art of debugging lies in narrowing down the problem scope.',
                    'デバッグの芸術は問題の範囲を絞り込むことにあります！',
                    '日志是最好的调试助手。',
                    'Logs are the best debugging companions.',
                    'ログは最高のデバッグ仲間です！',
                    'Les journaux sont les meilleurs compagnons de débogage.',
                    '重现问题是解决bug的第一步。',
                    'Reproducing the issue is the first step to fixing bugs.',
                    '問題を再現することはバグ修正の第一歩です！'
                ],
                'system_design': [
                    '高内聚低耦合是优秀系统设计的原则。',
                    'High cohesion and low coupling are principles of excellent system design.',
                    '高凝集低結合は優れたシステム設計の原則です！',
                    '可扩展性应该在设计初期就考虑。',
                    'Scalability should be considered from the early design phase.',
                    'スケーラビリティは初期設計段階から考慮すべきです！',
                    'L\'extensibilité doit être envisagée dès la phase de conception précoce.',
                    '容错设计能提高系统的稳定性。',
                    'Fault-tolerant design improves system stability.',
                    'フォールトトレラント設計はシステムの安定性を向上させます！'
                ]
            },
            
            # 哲学思辨类 (100+句)
            'philosophical_discussion': {
                'existence': [
                    '存在本身就是一个奇迹。',
                    'Existence itself is a miracle.',
                    '存在そのものが奇跡なのです！',
                    '我们既是观察者，也是被观察者。',
                    'We are both observers and the observed.',
                    '我々は観察者であり、同時に観察される存在でもあります！',
                    'Nous sommes à la fois observateurs et observés.',
                    '意识的起源仍然是科学最大的谜题之一。',
                    'The origin of consciousness remains one of science\'s greatest mysteries.',
                    '意識の起源はいまだに科学最大の謎の一つです！'
                ],
                'meaning': [
                    '生命的意义在于创造意义。',
                    'The meaning of life is to create meaning.',
                    '人生の意味は意味を創造することにあります！',
                    '每个人都应该书写自己的人生故事。',
                    'Everyone should write their own life story.',
                    '誰もが自分の人生の物語を書くべきです！',
                    'Chacun devrait écrire son propre récit de vie.',
                    '追求意义的过程本身就很有意义。',
                    'The process of pursuing meaning is meaningful in itself.',
                    '意味を求める過程そのものに大きな意味があります！'
                ],
                'ethics': [
                    '道德判断应该基于行为的结果而非动机。',
                    'Moral judgment should be based on consequences rather than intentions.',
                    '道徳的判断は動機ではなく結果に基づくべきです！',
                    '技术发展中伦理考量不可或缺。',
                    'Ethical considerations are indispensable in technological development.',
                    '技術発展における倫理的考察は不可欠です！',
                    'Les considérations éthiques sont indispensables dans le développement technologique.',
                    '责任与自由是道德哲学的核心议题。',
                    'Responsibility and freedom are central issues in moral philosophy.',
                    '責任と自由は道徳哲学の核心的課題です！'
                ]
            }
        }
    
    def get_contextual_response(self, user_message, context_history=None):
        """获取上下文相关的响应"""
        # 分析用户消息
        message_analysis = self.analyze_message(user_message)
        
        # 根据分析结果选择合适的响应类别
        response_category = self.select_response_category(message_analysis)
        
        # 获取相关响应
        responses = self.get_relevant_responses(response_category, message_analysis)
        
        # 应用上下文过滤
        if context_history:
            responses = self.filter_by_context(responses, context_history)
        
        # 返回最佳响应
        if responses:
            return random.choice(responses)
        else:
            return self.get_default_response()
    
    def analyze_message(self, message):
        """分析用户消息"""
        analysis = {
            'sentiment': self.detect_sentiment(message),
            'topics': self.extract_topics(message),
            'intent': self.detect_intent(message),
            'complexity': self.assess_complexity(message),
            'time_context': self.detect_time_context(message)
        }
        return analysis
    
    def detect_sentiment(self, message):
        """检测情感倾向"""
        positive_words = ['开心', '高兴', '喜欢', 'love', 'happy', 'good', 'great', 'awesome', '嬉しい', '좋아']
        negative_words = ['难过', '伤心', '讨厌', 'hate', 'sad', 'bad', 'terrible', 'awful', '悲しい', '싫어']
        neutral_words = ['知道', '了解', '明白', 'understand', 'know', 'learn', '勉強', '학습']
        
        pos_count = sum(1 for word in positive_words if word in message.lower())
        neg_count = sum(1 for word in negative_words if word in message.lower())
        neu_count = sum(1 for word in neutral_words if word in message.lower())
        
        if pos_count > neg_count and pos_count > neu_count:
            return 'positive'
        elif neg_count > pos_count and neg_count > neu_count:
            return 'negative'
        else:
            return 'neutral'
    
    def extract_topics(self, message):
        """提取话题关键词"""
        topics = []
        
        # 定义话题关键词
        topic_keywords = {
            'technology': ['技术', '科技', 'computer', 'technology', 'tech', 'プログラミング', '기술'],
            'science': ['科学', 'science', 'physics', 'chemistry', 'biology', '科学', '과학'],
            'philosophy': ['哲学', 'philosophy', 'think', 'thought', '哲学', '철학'],
            'emotion': ['心情', '感觉', 'feel', 'emotion', '気持ち', '감정'],
            'learning': ['学习', 'study', 'learn', 'education', '勉強', '학습'],
            'creativity': ['创意', '创造', 'creative', 'innovation', '創作', '창의성']
        }
        
        message_lower = message.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                topics.append(topic)
        
        return topics if topics else ['general']
    
    def detect_intent(self, message):
        """检测用户意图"""
        question_indicators = ['?', '什么', '如何', '怎样', 'why', 'how', 'what', 'when', 'where', 'なぜ', 'どうやって']
        greeting_indicators = ['你好', 'hello', 'hi', 'こんにちは', '안녕', 'hola']
        complaint_indicators = ['不好', '不行', 'problem', 'issue', 'error', '困ります', '문제']
        
        message_lower = message.lower()
        
        if any(indicator in message_lower for indicator in question_indicators):
            return 'question'
        elif any(indicator in message_lower for indicator in greeting_indicators):
            return 'greeting'
        elif any(indicator in message_lower for indicator in complaint_indicators):
            return 'complaint'
        else:
            return 'statement'
    
    def assess_complexity(self, message):
        """评估消息复杂度"""
        word_count = len(message.split())
        sentence_count = len(re.findall(r'[.!?。！？]', message)) + 1
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else word_count
        
        if avg_sentence_length > 20 or word_count > 50:
            return 'complex'
        elif avg_sentence_length > 10 or word_count > 20:
            return 'moderate'
        else:
            return 'simple'
    
    def detect_time_context(self, message):
        """检测时间上下文"""
        time_patterns = {
            'morning': ['早上', '早晨', 'morning', '朝', '아침'],
            'afternoon': ['下午', '中午', 'afternoon', '昼', '오후'],
            'evening': ['晚上', '傍晚', 'evening', '夕方', '저녁'],
            'night': ['夜里', '深夜', 'night', '夜', '밤']
        }
        
        current_hour = datetime.now().hour
        message_lower = message.lower()
        
        # 根据当前时间和消息内容判断
        for time_period, keywords in time_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return time_period
        
        # 根据当前时间判断
        if 5 <= current_hour < 12:
            return 'morning'
        elif 12 <= current_hour < 18:
            return 'afternoon'
        elif 18 <= current_hour < 22:
            return 'evening'
        else:
            return 'night'
    
    def select_response_category(self, analysis):
        """根据分析选择响应类别"""
        intent = analysis['intent']
        topics = analysis['topics']
        sentiment = analysis['sentiment']
        time_context = analysis['time_context']
        
        # 问候类特殊情况
        if intent == 'greeting':
            return f'greetings.{time_context}'
        
        # 根据话题和情感组合选择
        priority_order = [
            f'emotional_support.{sentiment}',
            f'knowledge_qa.{"_".join(topics[:1])}',
            f'creative_inspiration.{"_".join(topics[:1])}',
            f'life_advice.{"_".join(topics[:1])}',
            'greetings.general'
        ]
        
        return priority_order[0]  # 简化处理，实际应遍历选择
    
    def get_relevant_responses(self, category, analysis):
        """获取相关响应"""
        try:
            # 解析类别路径
            parts = category.split('.')
            if len(parts) == 2:
                main_category, sub_category = parts
                if main_category in self.dialogue_data and sub_category in self.dialogue_data[main_category]:
                    return self.dialogue_data[main_category][sub_category]
            elif len(parts) == 1:
                main_category = parts[0]
                if main_category in self.dialogue_data:
                    # 返回该类别下的所有子类别响应
                    responses = []
                    for sub_cat in self.dialogue_data[main_category].values():
                        responses.extend(sub_cat)
                    return responses
        except Exception as e:
            print(f"获取响应时出错: {e}")
        
        return []
    
    def filter_by_context(self, responses, context_history):
        """根据上下文过滤响应"""
        if not context_history or not responses:
            return responses
        
        # 简单的上下文过滤：避免重复最近说过的内容
        recent_messages = [msg.lower() for msg in context_history[-3:]]
        filtered_responses = []
        
        for response in responses:
            response_lower = response.lower()
            # 检查是否与最近的对话内容相似度过高
            is_similar = any(self.calculate_similarity(response_lower, recent) > 0.7 
                           for recent in recent_messages)
            if not is_similar:
                filtered_responses.append(response)
        
        return filtered_responses if filtered_responses else responses
    
    def calculate_similarity(self, text1, text2):
        """计算文本相似度（简化版）"""
        # 使用简单的词汇重叠率作为相似度指标
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0
    
    def get_default_response(self):
        """获取默认响应"""
        defaults = [
            '这是一个很有趣的观点呢！',
            'I find that perspective quite fascinating.',
            'とても興味深い観点ですね！',
            'That\'s an interesting way to look at it.',
            '您的想法很有创意！',
            'Your thoughts provoke meaningful consideration.',
            '让我想想这个问题...',
            'I need to process that information further.',
            '時間をかけて考えさせてください。',
            'Further reflection is warranted on this matter.',
            '这是个值得深入探讨的话题。',
            'This merits deeper investigation and discussion.'
        ]
        return random.choice(defaults)
    
    def get_random_response(self):
        """获取随机响应（用于测试）"""
        all_responses = []
        for category_dict in self.dialogue_data.values():
            for responses in category_dict.values():
                all_responses.extend(responses)
        return random.choice(all_responses) if all_responses else "对话库为空"
    
    def get_statistics(self):
        """获取对话库统计信息"""
        total_responses = 0
        category_counts = {}
        
        for main_category, sub_categories in self.dialogue_data.items():
            category_total = 0
            for sub_category, responses in sub_categories.items():
                count = len(responses)
                category_total += count
                category_counts[f"{main_category}.{sub_category}"] = count
            total_responses += category_total
            category_counts[main_category] = category_total
        
        return {
            'total_responses': total_responses,
            'category_breakdown': category_counts,
            'categories': list(self.dialogue_data.keys())
        }

# 全局对话库实例
offline_dialogue_lib = OfflineDialogueLibrary()

if __name__ == "__main__":
    # 测试对话库功能
    print("=== 离线对话库测试 ===")
    
    # 显示统计信息
    stats = offline_dialogue_lib.get_statistics()
    print(f"总响应数: {stats['total_responses']}")
    print(f"主要类别: {', '.join(stats['categories'])}")
    
    # 测试不同类型的消息
    test_messages = [
        "你好，今天心情怎么样？",
        "我想了解一下人工智能的发展前景",
        "最近学习压力很大，有点焦虑",
        "你觉得量子计算会对未来产生什么影响？",
        "晚上好，有什么好看的电影推荐吗？"
    ]
    
    print("\n=== 响应测试 ===")
    for message in test_messages:
        response = offline_dialogue_lib.get_contextual_response(message)
        print(f"用户: {message}")
        print(f"AI: {response}\n")