from deck import Deck
from hand_evaluator import HandEvaluator
from pot import Pot


class Dealer:
    """ディーラーを表すクラス。

    ゲームを進行させる役割を持っている。

    Attributes:
        deck (Deck): デッキのインスタンス。
        message_handler (MessageHandler): メッセージ処理のインスタンス。
        input_handler (InputHandler): 入力処理のインスタンス。
        pots (list[Pot]): メインポット、サイドポット。
        bet_record (list[int]): 直前のベット額の記録。
        community_cards (list[Card]): コミュニティカード。
        hand_evaluator (HandEvaluator): ハンド比較のインスタンス。

    Tests:
        [ ]: test_dealer

    """

    def __init__(self, message_handler, input_handler):
        """ディーラーを初期化する。

        新しいデッキを持ってゲームを開始する。

        Args:
            message_handler (MessageHandler): メッセージ処理のインスタンス。
            input_handler (InputHandler): 入力処理のインスタンス。

        """
        self.deck = Deck()
        self.message_handler = message_handler
        self.input_handler = input_handler
        self.pots = [Pot()]
        self.bet_record = []
        self.community_cards = []
        self.hand_evaluator = HandEvaluator()
        self.big_blind = 0

    def burn_card(self):
        """バーンカードを行う。
        """

        self.deck.draw()

    def deal_card(self, players, start_position=0):
        """プレイヤーにカードを配る。

        Args:
            players (list[Player]): プレイヤーのリスト
            start_potision (int, optional): カードをどこから配るか。デフォルト0。

        Tests:
            [ ]:
        """

        for i in range(len(players)):
            current_player = players[(start_position + i) % len(players)]
            current_player.hand.append(self.deck.draw())

    def set_initial_button(self, players):
        """ディーラーボタンの初期配置を決定する。

        Args:
            players (list[Player]): Playerクラスのインスタンスのリスト。

        Returns:
            Player: ディーラーボタンを持つプレイヤー。

        """

        # バーンカード処理
        self.burn_card()

        # 各プレイヤーにカードを1枚ずつ配る
        self.deal_card(players)

        self.message_handler.display_players_info(players, ["PlayerName", "Hand"])

        # 最も高いカードを持っているプレイヤーを特定
        dealer_player = max(players, key=lambda player: (player.hand[0].rank, player.hand[0].suit))

        # 一時的に持たせたカードを削除
        for player in players:
            player.hand.pop()

        dealer_player.is_dealer = True
        return dealer_player

    def get_dealer_button_index(self, players, count=0):
        """ディーラーボタンからいくつ隣かを返す。

        Args:
            players (list[Player]): プレイヤーのリスト。
            count (int, optional): いくつ隣か。

        Tests:
            [ ]:
        """
        return [player.is_dealer for player in players].index(True) + count

    def deal_hole_cards(self, players):
        """各プレイヤーに2枚のホールカードを配るメソッド。

        Args:
            players (list[Player]): Playerクラスのインスタンスのリスト。

        """
        # バーンカード
        self.burn_card()

        # ディーラーボタンの位置を取得
        dealer_position = self.get_dealer_button_index(players)

        # 配る開始位置を決定
        start_position = (dealer_position + 1) % len(players)

        # 1枚目のカードを全プレイヤーに配る
        self.deal_card(players, start_position)

        # 2枚目のカードを全プレイヤーに配る
        self.deal_card(players, start_position)

    def set_action_list(self, player, bet_record, current_max_bet, bet_type):
        """プレイヤーごとのアクションリストを作成。

        Args:
            player (Player): アクションを行うプレイヤー。
            bet_record (list[str]): 全プレイヤーのアクションの履歴。
            current_max_bet (int): 現在の最大賭け金。
            bet_type (str): ベットタイプ。

        Returns:
            list: 実行できるアクションが入ったリスト

        Tests:
            [ ]:
        """

        action_list = ["fold"]

        if len(bet_record) >= 2:
            # プレイヤーがコールするためのチップが不足している場合、オールイン
            if player.chips <= current_max_bet - player.current_bet:
                action_list.append("all-in")
            else:
                action_list.append("call")

            # 他のプレイヤーが全額ベットしていない場合、レイズが可能
            if current_max_bet < player.current_bet + player.chips:
                if bet_type != "fix" or len(bet_record) <= 4:
                    action_list.append("raise")
        else:
            action_list.append("check")

            # 他のプレイヤーが全額ベットしていない場合、ベットが可能
            if current_max_bet < player.current_bet + player.chips:
                if bet_type != "fix" or len(bet_record) <= 4:
                    action_list.append("bet")

        return action_list

    def selected_action(self, action, player, current_max_bet, bb_value, bet_type, bet_round):
        """選択されたアクションによってプレイヤーの状態を変化させるメソッド。

        Args:
            action (str): 選択されたアクション。
            player (Player): アクションを選択したプレイヤー。
            current_max_bet (int): 現在の最大賭け金。
            bb_value (int): BBの値。
            bet_type (str): ベットタイプ。
            bet_round (str): ベットラウンド。

        Tests:
            [ ]:
        """

        if action == "fold":
            player.fold()
            player.last_action.append("Fold")

        elif action == "check":
            player.last_action.append("Check")

        elif action == "call":
            call_amount = current_max_bet - player.current_bet
            player.bet(call_amount)
            player.last_action.append("Call")

        elif action == "bet":
            # 最低ベット額はビッグブラインド
            if bet_type == "no":
                # no_limit
                min_bet = self.big_blind * 2 - player.current_bet
            # プレイヤーのチップがmin_betよりも少ない場合、プレイヤーのチップをmin_betとする
            # 最低ベット額はビッグブラインド
            if bet_type == "no":
                # no_limit
                max_bet = player.chips
            if bet_type != "fix":
                if player.chips < min_bet:
                    min_bet = player.chips
            if bet_type != "fix":
                bet_amount = player.select_bet_amount(min_bet, max_bet)
            else:
                if bet_round == "pre_flop" or bet_round == "flop":
                    if len(self.bet_record) > 0:
                        bet_amount = self.bet_record[-1] + bb_value - player.current_bet
                    else:
                        bet_amount = bb_value - player.current_bet
                else:
                    if len(self.bet_record) > 0:
                        bet_amount = self.bet_record[-1] + bb_value * 2 - player.current_bet
                    else:
                        bet_amount = bb_value * 2 - player.current_bet
            if bet_amount == player.chips:
                player.is_all_in = True
                player.last_action.append("All-In")
            else:
                player.last_action.append("Bet")
            player.bet(bet_amount)
            # raise_difference = bet_amount
            current_max_bet = bet_amount
            self.bet_record.append(player.current_bet)
            # previous_player_bet_or_raise = bet_amount
            player.last_bet_amount = bet_amount

        elif action == "raise":
            # 配列の最後とその１個前の値を引き算する。
            if bet_type == "no":
                min_raise = self.bet_record[-1] - self.bet_record[-2] + self.bet_record[-1] - player.current_bet

            if bet_type == "no":
                max_raise = player.chips

            # プレイヤーのチップがmin_raiseよりも少ない場合、プレイヤーのチップをmin_raiseとする
            if bet_type != "fix":
                if player.chips < min_raise:
                    min_raise = player.chips

            # プレイヤーにミニマムレイズ額以上のレイズ額を選択させる
            if bet_type != "fix":
                raise_amount = player.select_bet_amount(min_raise, max_raise)
            else:
                if bet_round == "pre_flop" or bet_round == "flop":
                    raise_amount = self.bet_record[-1] + bb_value - player.current_bet
                else:
                    raise_amount = self.bet_record[-1] + bb_value * 2 - player.current_bet

            # プレイヤーのベットを更新
            current_max_bet = raise_amount

            if raise_amount == player.chips:
                player.is_all_in = True
                player.last_action.append("All-In")
            else:
                player.last_action.append("Raise")
            player.bet(raise_amount)
            self.bet_record.append(player.current_bet)

            player.last_bet_amount = raise_amount

        elif action == "all-in":
            all_in_amount = player.chips
            player.bet(all_in_amount)
            player.last_action.append("All-In")
            player.is_all_in = True
            if all_in_amount > current_max_bet:
                current_max_bet = all_in_amount
                player.last_bet_amount = all_in_amount

    def bet_round(self, players, big_blind, bb_value, bet_type, bet_round):
        """ベットラウンドのアクションを処理する。

        ディーラーボタンの3つ隣からアクションを開始し、すべてのプレイヤーが
        同じベット額になるか、すべてのプレイヤーがアクションを完了するまで続行する。

        Args:
            players (list[Player]): Playerクラスのインスタンスのリスト。
            big_blind (int): ビッグブラインド。
            bb_value (int): BBの値。
            bet_type (str): ベットタイプ。
            bet_round (str): ベットラウンド。

        Returns:
            list[Player]: この先もアクションをする人のリスト。

        """
        self.big_blind = big_blind
        # アクション開始位置をディーラーボタンの3つ隣からに設定
        start_index = self.get_dealer_button_index(players, 3)
        start_index %= len(players)

        for player in players:
            player.has_acted = False

        while True:

            # アクティブなプレイヤーが1人だけになった場合、アクションを終了
            for i in range(len(players)):
                current_index = (start_index + i) % len(players)
                player = players[current_index]

                active_players = [player for player in players if not player.is_folded]

                # ある一人以外全員フォールドした場合
                if len(active_players) == 1:
                    # そのプレイヤーが勝ったので、勝利判定に進む
                    return active_players

                if player.is_folded:
                    continue

                # アクションの終了条件を確認
                all_players_all_in = all(player.is_all_in for player in active_players if not player.is_folded)
                if all_players_all_in:
                    return active_players

                if player.is_all_in:  # オール・インしたプレイヤーはアクションを取らない
                    continue

                # 現在の最大掛け金取得
                current_max_bet = max([player.current_bet for player in players])

                action_list = self.set_action_list(player, self.bet_record, current_max_bet, bet_type)

                # プレイヤーのアクション選択
                action = player.select_action(action_list)

                self.selected_action(action, player, current_max_bet, bb_value, bet_type, bet_round)

                player.has_acted = True

                self.message_handler.display_community_cards(self.community_cards, sum(pot.total for pot in self.pots))

                self.message_handler.display_players_info(players)

                self.input_handler.wait_for_user()

                active_players = [player for player in players if not player.is_folded]

                if action in ["bet", "raise", "all-in"]:
                    for other_player in active_players:
                        if other_player != player:
                            other_player.has_acted = False

                active_players_bet = {player.current_bet for player in active_players if not player.is_folded}
                active_players_acted = all(player.has_acted or player.is_all_in for player in active_players if not player.is_folded)

                if len(active_players_bet) >= 1 and active_players_acted:
                    # ポットの回収、フロップの公開に進む
                    self.bet_record = [0]
                    return active_players

                # すべてのアクティブプレイヤーがオール・インしたかどうかをチェック
                all_in_players = [player for player in active_players if player.is_all_in]
                if len(all_in_players) == len(active_players) and active_players_acted:
                    self.bet_record = [0]
                    return active_players

    def pot_collect(self, players):
        """プレイヤーの賭け金をポットとして集める。

        Args:
            players (list[Player]): Playerクラスのインスタンスのリスト。

        Returns:
            int: ポットの合計値。

        """
        active_bets = sorted({player.current_bet for player in players if not player.is_folded})

        last_bet = 0
        for index, bet in enumerate(active_bets):
            # 最初のポット（メインポット）であれば既存のものを使用、それ以外は新しいポットを作成
            if index == 0:
                pot = self.pots[0]
            else:
                pot = Pot()
                self.pots.append(pot)

            for player in players:
                contribution = min(bet - last_bet, player.current_bet)
                if contribution > 0:
                    pot.add_contribution(player, contribution)
                    player.current_bet -= contribution

            last_bet = bet

        # プレイヤーの現在のベットが0でない場合、残りを新しいサイドポットに追加
        for player in players:
            if player.current_bet > 0:
                if not self.pots or player.current_bet > self.pots[-1].total:
                    pot = Pot()
                    self.pots.append(pot)
                pot.add_contribution(player, player.current_bet)
                player.current_bet = 0

            player.last_action = []

        return sum(pot.total for pot in self.pots)

    def reveal_community_cards(self, num_cards):
        """指定された枚数のコミュニティカードを公開する。

        Args:
            num_cards (int): 公開するカードの枚数

        Returns:
            list[Card]: コミュニティカード。

        """
        self.burn_card()

        for _ in range(num_cards):
            card = self.deck.draw()  # デッキからカードを1枚引く
            self.community_cards.append(card)

        return self.community_cards

    def distribute_pots(self, active_players):
        """アクティブなプレイヤーの手同士を評価し、ポットを分配する。

        Args:
            active_players (list[Player]): アクティブなプレイヤーのリスト。

        """
        ranked_players = sorted(active_players, key=lambda player: (player.hand_category.strength, player.hand_rank), reverse=True)

        for index, pot in enumerate(self.pots):
            involved_players = list(pot.contributions.keys())
            eligible_players = [player for player in ranked_players if player in involved_players]

            # 一番強い手を持つプレイヤーが複数いる場合、ポットを分割
            winners = [player for player in eligible_players if player.hand_category == eligible_players[0].hand_category
                       and player.hand_rank == eligible_players[0].hand_rank]

            total_in_this_pot = sum(pot.contributions.values())

            if index == 0:
                self.message_handler.get_message("main_pot")
            else:
                self.message_handler.get_message("side_pot", index=index)

            for winner in winners:
                get_chips = total_in_this_pot // len(winners)
                winner.chips += get_chips
                self.message_handler.get_message("win_player", player_name=winner.name, get_chips=get_chips, chips=winner.chips)

    def evaluate_and_fold_players(self, active_players):
        """アクティブなプレイヤーの手を評価する。

        Args:
            active_players (list[Player]): アクティブなプレイヤーのリスト。

        """
        for player in active_players:
            player.hand_category, player.hand_rank = self.hand_evaluator.evaluate_hand(player.hand, self.community_cards)
            self.message_handler.get_message("player_best_hand", player_name=player.name,
                                             hand_category=player.hand_category.name_jp, hand_rank=player.hand_rank)

        # ポットを分配
        self.distribute_pots(active_players)

    def distribute_pot(self, players):
        """勝ったプレイヤーにポットを渡す。

        Args:
            players (list[Player]): プレイヤーのリスト。

        """

        # 改めてフォールドしていないプレイヤーのリストを作成
        non_folded_players = [player for player in players if not player.is_folded]

        # ポットをフォールドしていないプレイヤーに渡す
        get_chips = sum(pot.total for pot in self.pots)
        for player in non_folded_players:
            player.chips += get_chips
            self.message_handler.get_message("win_player", player_name=player.name, get_chips=get_chips, chips=player.chips)

    def reset_round(self, players):
        """ラウンドの終了後に必要な情報をリセットする。

        Args:
            players (list[Player]): Playerクラスのインスタンスのリスト。

        """
        # 1. 各プレイヤーのカレントベットと手札をリセット
        for player in players:
            player.hand = []
            player.current_bet = 0  # 現在のベット額。
            player.last_action = []  # 最後のアクションを保存する属性
            player.last_bet_amount = 0
            player.has_acted = False
            player.is_folded = False  # プレイヤーがフォールドしたかどうかを示すフラグ。
            player.is_all_in = False
            player.hand_category = None
            player.hand_rank = None

        # 2. コミュニティカードのリセット
        self.community_cards = []

        # 3. ポットのリセット
        self.pots = [Pot()]

        # 4. 別途履歴のリセット
        self.bet_record = []

        # 5. デッキのリセット
        self.deck = Deck()

        # n. その他の必要な情報をリセット
        # 必要に応じて追加してください。

    def move_dealer_button(self, players):
        """ディーラーボタンを次のプレイヤーに移動します。

        Args:
            players (list[Player]): Playerクラスのインスタンスのリスト。

        """
        # 現在のディーラーの位置を取得
        current_dealer_index = self.get_dealer_button_index(players)

        # 現在のディーラーのフラグをFalseにする
        players[current_dealer_index].is_dealer = False

        # 次のディーラーの位置を計算
        next_dealer_index = (current_dealer_index + 1) % len(players)

        # 次のディーラーのフラグをTrueにする
        players[next_dealer_index].is_dealer = True
