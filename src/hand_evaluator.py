from enum import Enum, auto
from itertools import combinations


class HandCategory(Enum):
    """
    ハンドカテゴリの強さと日本語名を定義するクラス。
    """
    HIGH_CARD = ("ハイカード", auto())
    ONE_PAIR = ("ワンペア", auto())
    TWO_PAIR = ("ツーペア", auto())
    THREE_OF_A_KIND = ("スリーカード", auto())
    STRAIGHT = ("ストレート", auto())
    FLUSH = ("フラッシュ", auto())
    FULL_HOUSE = ("フルハウス", auto())
    FOUR_OF_A_KIND = ("フォーカード", auto())
    STRAIGHT_FLUSH = ("ストレートフラッシュ", auto())
    ROYAL_FLUSH = ("ロイヤルフラッシュ", auto())

    def __init__(self, name_jp, strength):
        self.name_jp = name_jp
        self.strength = strength


class HandEvaluator:
    """
    ハンドの強さを比較するクラス。
    """
    RANKS = {str(i): i for i in range(2, 11)}
    RANKS.update({"J": 11, "Q": 12, "K": 13, "A": 14})

    def __init__(self):
        pass

    def evaluate_hand(self, player_hand, community_cards):
        """
        プレイヤーの手とコミュニティカードからもっとも強い５枚を選定し、そのハンドのカテゴリトランクを返すメソッド。

        Parameters:
        - player_hand (list): 2枚のカードのリスト。
        - community_cards (list): 5枚のカードのリスト。

        Returns:
        - tuple: そのプレイヤー最も強いハンドカテゴリとそのランク。
        """
        combined_cards = player_hand + community_cards
        best_category, best_rank = self.best_hand_from_seven(combined_cards)
        return best_category, best_rank

    def best_hand_from_seven(self, cards):
        """
        7枚のカードから最も強い5枚の手を構築します。

        Parameters:
        - seven_cards (list): 7枚のカードのリスト。

        Returns:
        - tuple: そのプレイヤー最も強いハンドカテゴリとそのランク。
        """
        best_category = None
        best_rank = None
        for five_cards in combinations(cards, 5):
            category, rank = self.evaluate_five(five_cards)
            if best_category is None:
                best_category, best_rank = category, rank
            if category.strength > best_category.strength:
                best_category, best_rank = category, rank
            if category == best_category and rank > best_rank:
                best_category, best_rank = category, rank

        return best_category, best_rank

    def evaluate_five(self, cards):
        """
        各ハンドカテゴリの評価メソッドを順に試すメソッド。

        Parameters:
        - seven_cards (list): 5枚のカードのリスト。

        Returns:
        - tuple: 渡されたハンドのカテゴリとそのランク。
        """
        for hand_evaluator in [self.is_royal_flush, self.is_straight_flush, self.is_four_of_a_kind, self.is_full_house,
                               self.is_flush, self.is_straight, self.is_three_of_a_kind, self.is_two_pair,
                               self.is_one_pair, self.is_high_card]:
            result = hand_evaluator(cards)
            if result[0] is not None:
                return result
        return None, None

    def is_royal_flush(self, cards):
        """
        ロイヤルフラッシュかどうかを判定します。

        Parameters:
        - cards (list): カードクラスのインスタンスのリスト。

        Returns:
        - tuple: (ハンドカテゴリ, ランク) または (None, None)
        """
        straight_flush_result = self.is_straight_flush(cards)
        if straight_flush_result[0] is not None:
            if straight_flush_result[0].strength == HandCategory.STRAIGHT_FLUSH.strength:
                ranks = sorted([self.RANKS[card.rank] for card in cards], reverse=True)
                if ranks[:5] == [self.RANKS[rank] for rank in ["A", "K", "Q", "J", "10"]]:
                    return (HandCategory.ROYAL_FLUSH, None)
        return (None, None)

    def is_straight_flush(self, cards):
        """
        ストレートフラッシュかどうかを判定します。

        Parameters:
        - cards (list): カードクラスのインスタンスのリスト。

        Returns:
        - tuple: (ハンドカテゴリ, ランク) または (None, None)
        """
        flush_result = self.is_flush(cards)
        straight_result = self.is_straight(cards)
        if flush_result[0] is not None and straight_result[0] is not None:
            if flush_result[0].strength == HandCategory.FLUSH.strength and straight_result[0].strength == HandCategory.STRAIGHT.strength:
                return (HandCategory.STRAIGHT_FLUSH, straight_result[1])
        return (None, None)

    def is_four_of_a_kind(self, cards):
        """
        フォーカードかどうかを判定します。

        Parameters:
        - cards (list): カードクラスのインスタンスのリスト。

        Returns:
        - tuple: (ハンドカテゴリ, ランク) または (None, None)
        """
        rank_counts = self.get_rank_counts(cards)
        four_of_a_kind_rank = [rank for rank, count in rank_counts.items() if count == 4]
        if four_of_a_kind_rank:
            kicker_ranks = sorted([self.RANKS[card.rank] for card in cards if card.rank != four_of_a_kind_rank[0]], reverse=True)
            return (HandCategory.FOUR_OF_A_KIND, [self.RANKS[four_of_a_kind_rank[0]]] + kicker_ranks)
        return (None, None)

    def is_full_house(self, cards):
        """
        フルハウスかどうかを判定します。

        Parameters:
        - cards (list): カードクラスのインスタンスのリスト。

        Returns:
        - tuple: (ハンドカテゴリ, ランク) または (None, None)
        """
        rank_counts = self.get_rank_counts(cards)
        three_of_a_kind_rank = [self.RANKS[rank] for rank, count in rank_counts.items() if count == 3]
        one_pair_rank = [self.RANKS[rank] for rank, count in rank_counts.items() if count == 2]
        if three_of_a_kind_rank and one_pair_rank:
            return (HandCategory.FULL_HOUSE, [three_of_a_kind_rank[0], one_pair_rank[0]])
        return (None, None)

    def is_flush(self, cards):
        """
        フラッシュかどうかを判定します。

        Parameters:
        - cards (list): カードクラスのインスタンスのリスト。

        Returns:
        - tuple: (ハンドカテゴリ, ランク) または (None, None)
        """
        suits = [card.suit for card in cards]
        if len(set(suits)) == 1:
            rank = sorted([self.RANKS[card.rank] for card in cards], reverse=True)
            return (HandCategory.FLUSH, rank)
        return (None, None)

    def is_straight(self, cards):
        """
        ストレートかどうかを判定します。

        Parameters:
        - cards (list): カードクラスのインスタンスのリスト。

        Returns:
        - tuple: (ハンドカテゴリ, ランク) または (None, None)
        """
        # カードのランクをセットに変換
        ranks = set([self.RANKS[card.rank] for card in cards])

        # ストレートを検出する
        for top_rank in range(14, 4, -1):  # 14はAceのランク
            straight = {top_rank - i for i in range(5)}
            if straight <= ranks:  # straightがranksのサブセットであるかをチェック
                # 最高ランクのカードを返す
                return (HandCategory.STRAIGHT, top_rank)

        # A-2-3-4-5のストレートを特別にチェック
        if ranks >= {14, 2, 3, 4, 5}:
            return (HandCategory.STRAIGHT, 5)

        return (None, None)

    def is_three_of_a_kind(self, cards):
        """
        スリーカードかどうかを判定します。

        Parameters:
        - cards (list): カードクラスのインスタンスのリスト。

        Returns:
        - tuple: (ハンドカテゴリ, ランク) または (None, None)
        """
        rank_counts = self.get_rank_counts(cards)
        three_of_a_kind_rank = [self.RANKS[rank] for rank, count in rank_counts.items() if count == 3]
        if three_of_a_kind_rank:
            kicker_ranks = sorted([self.RANKS[card.rank] for card in cards if self.RANKS[card.rank] != three_of_a_kind_rank[0]], reverse=True)
            return (HandCategory.THREE_OF_A_KIND, [three_of_a_kind_rank[0]] + kicker_ranks[:2])
        return (None, None)

    def is_two_pair(self, cards):
        """
        ツーペアかどうかを判定します。

        Parameters:
        - cards (list): カードクラスのインスタンスのリスト。

        Returns:
        - tuple: (ハンドカテゴリ, ランク) または (None, None)
        """
        rank_counts = self.get_rank_counts(cards)
        pairs = [self.RANKS[rank] for rank, count in rank_counts.items() if count == 2]
        if len(pairs) >= 2:
            kicker_ranks = sorted([self.RANKS[card.rank] for card in cards if self.RANKS[card.rank] not in pairs], reverse=True)
            return (HandCategory.TWO_PAIR, sorted(pairs, reverse=True) + [kicker_ranks[0]])
        return (None, None)

    def is_one_pair(self, cards):
        """
        ワンペアかどうかを判定します。

        Parameters:
        - cards (list): カードクラスのインスタンスのリスト。

        Returns:
        - tuple: (ハンドカテゴリ, ランク) または (None, None)
        """
        rank_counts = self.get_rank_counts(cards)
        pairs = [self.RANKS[rank] for rank, count in rank_counts.items() if count == 2]
        if pairs:
            kicker_ranks = sorted([self.RANKS[card.rank] for card in cards if self.RANKS[card.rank] != pairs[0]], reverse=True)
            return (HandCategory.ONE_PAIR, [pairs[0]] + kicker_ranks[:3])
        return (None, None)

    def is_high_card(self, cards):
        """
        ハイカードかどうかを判定します。

        Parameters:
        - cards (list): カードクラスのインスタンスのリスト。

        Returns:
        - tuple: (ハンドカテゴリ, ランク) または (None, None)
        """
        ranks = sorted([self.RANKS[card.rank] for card in cards], reverse=True)
        return (HandCategory.HIGH_CARD, ranks[:5])

    def get_rank_counts(self, sorted_combination):
        """
        各ランクのカウントを取得する。

        Parameters:
        - sorted_combination (list): ソートされたカードの組み合わせ。

        Returns:
        - dict: 各ランクのカウント。
        """
        rank_counts = {}
        for card in sorted_combination:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
        return rank_counts
