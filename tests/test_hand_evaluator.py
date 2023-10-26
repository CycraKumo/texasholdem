import pytest
from itertools import combinations
import random

from card import Card
from hand_evaluator import HandEvaluator, HandCategory


evaluator = HandEvaluator()

SUITS = ["♤", "♡", "♢", "♧"]
RANKS = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
STRAIGHT_RANKS = ["K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
RANKS_NUMBER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}


def get_cards(suits=SUITS, ranks=RANKS):
    """
    指定されたスートとランクのカードのリストを返します。

    Args:
        suits (list[str]): 使用するスートのリスト。指定しない場合、すべてのスートが使用されます。
        ranks (list[str]): 使用するランクのリスト。指定しない場合、すべてのランクが使用されます。

    Returns:
        list[Card]: 指定されたスートとランクのカードのリスト。

    """
    return [Card(suit, rank) for suit in suits for rank in ranks]


def generate_straights():
    for i in range(len(STRAIGHT_RANKS) - 4):
        yield STRAIGHT_RANKS[i:i+5]


def get_cards_from_ranks(ranks):
    suits = SUITS
    return [Card(suits[i % 4], rank) for i, rank in enumerate(ranks)]


@pytest.mark.parametrize("suit", SUITS)
def test_royal_flush(suit):
    """ロイヤルストレートフラッシュであることを確認

    """
    hand = get_cards(suit, ["A", "K", "Q", "J", "10"])
    category, rank = evaluator.evaluate_five(hand)
    assert category.strength == HandCategory.ROYAL_FLUSH.strength


@pytest.mark.parametrize("suit", SUITS)
def test_non_royal_flush(suit):
    """ロイヤルストレートフラッシュでないことを確認

    """
    hand = get_cards([suit], ["A", "K", "Q", "J", "9"])
    category, rank = evaluator.evaluate_five(hand)
    assert category.strength != HandCategory.ROYAL_FLUSH.strength


@pytest.mark.parametrize("suit", SUITS)
def test_max_straight_flush(suit):
    """ストレートフラッシュの最高ランクであることを確認

    """
    hand = get_cards(suit, ["K", "Q", "J", "10", "9"])
    category, rank = evaluator.evaluate_five(hand)
    assert category.strength == HandCategory.STRAIGHT_FLUSH.strength
    assert rank == 13


@pytest.mark.parametrize("suit", SUITS)
def test_min_straight_flush(suit):
    """ストレートフラッシュの最低ランクであることを確認

    """
    hand = get_cards(suit, ["5", "4", "3", "2", "A"])
    category, rank = evaluator.evaluate_five(hand)
    assert category.strength == HandCategory.STRAIGHT_FLUSH.strength
    assert rank == 5


@pytest.mark.parametrize("suit", SUITS)
def test_middle_straight_flush(suit):
    """ストレートフラッシュの中間ランクであることを確認

    """
    for straight in generate_straights():
        hand = get_cards(suit, straight)
        category, rank = evaluator.evaluate_five(hand)
        assert category.strength == HandCategory.STRAIGHT_FLUSH.strength
        assert rank == RANKS_NUMBER[straight[0]]


@pytest.mark.parametrize("suit", SUITS)
def test_non_straight_flush(suit):
    """ストレートフラッシュでないことを確認

    """
    hand = get_cards([suit], ["K", "Q", "J", "10", "8"])
    category, rank = evaluator.evaluate_five(hand)
    assert category.strength != HandCategory.STRAIGHT_FLUSH.strength


@pytest.mark.parametrize("rank", RANKS)
def test_four_of_a_kind(rank):
    """4カードであることを確認

    """
    hand = get_cards(["♤", "♡", "♢", "♧"], [rank])

    if rank == "A":
        kicker_card = Card("♤", "2")
    else:
        kicker_card = Card("♤", "A")

    hand.append(kicker_card)

    category, hand_rank = evaluator.evaluate_five(hand)
    assert category.strength == HandCategory.FOUR_OF_A_KIND.strength
    assert hand_rank == [RANKS_NUMBER[rank], RANKS_NUMBER[kicker_card.rank]]


@pytest.mark.parametrize("three_rank, two_rank", [(r1, r2) for r1 in RANKS for r2 in RANKS if r1 != r2])
def test_full_house(three_rank, two_rank):
    """フルハウスであることを確認

    """
    hand = get_cards(["♤", "♡", "♢"], [three_rank]) + get_cards(["♤", "♡"], [two_rank])
    category, rank = evaluator.evaluate_five(hand)
    assert category.strength == HandCategory.FULL_HOUSE.strength
    assert rank == [RANKS_NUMBER[three_rank], RANKS_NUMBER[two_rank]]


@pytest.mark.parametrize("suit", SUITS)
@pytest.mark.parametrize("ranks", [r for r in combinations(RANKS, 5) if not evaluator.is_straight([Card("♤", rank) for rank in r])[0]])
def test_flush(suit, ranks):
    """フラッシュであることを確認

    """
    hand = get_cards(suit, ranks)
    category, rank = evaluator.evaluate_five(hand)
    assert category.strength == HandCategory.FLUSH.strength
    assert rank == [RANKS_NUMBER[r] for r in ranks]


@pytest.mark.parametrize("ranks, top_rank", [
    (["A", "2", "3", "4", "5"], 5),
    (["2", "3", "4", "5", "6"], 6),
    (["3", "4", "5", "6", "7"], 7),
    (["4", "5", "6", "7", "8"], 8),
    (["5", "6", "7", "8", "9"], 9),
    (["6", "7", "8", "9", "10"], 10),
    (["7", "8", "9", "10", "J"], 11),
    (["8", "9", "10", "J", "Q"], 12),
    (["9", "10", "J", "Q", "K"], 13),
    (["10", "J", "Q", "K", "A"], 14),
])
def test_straight(ranks, top_rank):
    """境界値と中間のランクのストレートであることを確認

    """
    hand = get_cards_from_ranks(ranks)
    category, rank = evaluator.evaluate_five(hand)
    assert category.strength == HandCategory.STRAIGHT.strength
    assert rank == top_rank


@pytest.mark.parametrize("ranks", [
    ["A", "2", "3", "5", "6"],
    ["2", "3", "4", "6", "7"],
    ["10", "J", "Q", "A", "2"]
])
def test_not_straight(ranks):
    """ストレートでないことを確認

    """
    hand = get_cards_from_ranks(ranks)
    category, _ = evaluator.evaluate_five(hand)
    assert category.strength != HandCategory.STRAIGHT.strength


@pytest.mark.parametrize("triple_rank", ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"])
def test_three_of_a_kind(triple_rank):
    """スリー・オブ・ア・カインドであることを確認

    """
    # 3枚の同じランクのカードを取得
    triple_cards = get_cards_from_ranks([triple_rank, triple_rank, triple_rank])

    # 他の2枚のカードを適当に取得（ただし、3枚と同じランクでないように）
    other_ranks = [rank for rank in RANKS if rank != triple_rank]
    sampled_other_ranks = random.sample(other_ranks, 2)
    other_cards = get_cards_from_ranks(sampled_other_ranks)

    # ハンドを組み合わせる
    hand = triple_cards + other_cards

    # 評価を行う
    category, rank = evaluator.evaluate_five(hand)
    assert category.strength == HandCategory.THREE_OF_A_KIND.strength
    assert rank[0] == HandEvaluator.RANKS[triple_rank]
    assert sorted(rank[1:]) == sorted([HandEvaluator.RANKS[r] for r in sampled_other_ranks])


@pytest.mark.parametrize("pair1_rank, pair2_rank", combinations(RANKS, 2))
def test_two_pair(pair1_rank, pair2_rank):
    """ツーペアであることを確認

    """
    # 2組のペアのカードを取得
    pair1_cards = get_cards_from_ranks([pair1_rank, pair1_rank])
    pair2_cards = get_cards_from_ranks([pair2_rank, pair2_rank])

    # 他の1枚のカードを適当に取得（ただし、ペアと同じランクでないように）
    other_ranks = [rank for rank in RANKS if rank != pair1_rank and rank != pair2_rank]
    other_card_rank = random.choice(other_ranks)
    other_card = get_cards_from_ranks([other_card_rank])

    # ハンドを組み合わせる
    hand = pair1_cards + pair2_cards + other_card

    # 評価を行う
    category, rank = evaluator.evaluate_five(hand)
    assert category.strength == HandCategory.TWO_PAIR.strength
    assert set(rank[:2]) == {HandEvaluator.RANKS[pair1_rank], HandEvaluator.RANKS[pair2_rank]}
    assert rank[2] == HandEvaluator.RANKS[other_card_rank]


@pytest.mark.parametrize("pair_rank", HandEvaluator.RANKS.keys())
def test_one_pair(pair_rank):
    """ワンペアであることを確認

    """
    # ペアのカードを取得
    pair_cards = get_cards_from_ranks([pair_rank, pair_rank])

    # 他の3枚のカードを適当に取得（ただし、ペアと同じランクでないように）
    other_ranks = [rank for rank in RANKS if rank != pair_rank]
    other_cards = get_cards_from_ranks(random.sample(other_ranks, 3))

    # ハンドを組み合わせる
    hand = pair_cards + other_cards

    # 評価を行う
    category, rank = evaluator.evaluate_five(hand)
    assert category.strength == HandCategory.ONE_PAIR.strength
    assert rank[0] == HandEvaluator.RANKS[pair_rank]
    assert sorted(rank[1:4]) == sorted([HandEvaluator.RANKS[card.rank] for card in other_cards])


def test_high_card():
    """ハイカードであることを確認

    """
    # 5枚の異なるランクのカードを取得
    hand_ranks = random.sample(RANKS, 5)
    hand = get_cards_from_ranks(hand_ranks)

    # 評価を行う
    category, rank = evaluator.evaluate_five(hand)

    # ハンドのランクを降順にソート
    sorted_hand_ranks = sorted([RANKS_NUMBER[r] for r in hand_ranks], reverse=True)

    assert category.strength == HandCategory.HIGH_CARD.strength
    assert rank == sorted_hand_ranks


def test_individual_check():
    """スリー・オブ・ア・カインドであることを確認

    """
    hand = [Card("♢", "A"), Card("♡", "A")]
    community_card = [Card("♤", "A"), Card("♡", "2"), Card("♤", "Q"), Card("♤", "8"), Card("♧", "7")]

    category, rank = evaluator.evaluate_hand(hand, community_card)

    assert category.strength == HandCategory.THREE_OF_A_KIND.strength
