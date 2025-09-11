from typing import List, Optional, Iterable, Tuple
import csv
# ----------------- Regras do jogo -----------------
WIN_LINES = [
    (0,1,2), (3,4,5), (6,7,8),     # linhas
    (0,3,6), (1,4,7), (2,5,8),     # colunas
    (0,4,8), (2,4,6)               # diagonais
]
class DataSet_Maker():
    
    def __init__(self):
        pass
    
    def check_win(self,board: List[str], p: str) -> bool:
        return any(all(board[i] == p for i in line) for line in WIN_LINES)

    def terminal(self,board: List[str]) -> bool:
        return self.check_win(board, '1') or self.check_win(board, '-1') or ('0' not in board)

    def proximo_jogador(self,board: List[str]) -> str:
        cx, co = board.count('1'), board.count('-1')
        return '1' if cx == co else '-1'

    def classificar(self,board: List[str]) -> str:
        if self.terminal(board):
            return "Fim_de_jogo"
        pj = self.proximo_jogador(board)
        for i, v in enumerate(board):
            if v == '0':
                board[i] = pj
                if self.terminal(board):
                    board[i] = '0'
                    return "Possibilidade_de_fim_de_jogo"
                board[i] = '0'
        return "Em_jogo"

    def linha_txt(self,board: List[str], classe: str) -> str:
        return ";".join(board) + ";" + classe

    # ----------------- Geração de todas as partidas -----------------
    def gerar_partidas(self,primeiro: str = '1') -> Iterable[Tuple[List[int], List[str], Optional[str]]]:
        board = ['0'] * 9
        vazias = list(range(9))

        def dfs(turn: int, seq: List[int], atual: str):
            if turn > 0:
                ultimo = '-1' if atual == '1' else '1'
                if self.check_win(board, ultimo):
                    yield (seq[:], board[:], ultimo)
                    return

            if not vazias:
                yield (seq[:], board[:], None)
                return

            prox = '-1' if atual == '1' else '1'
            for idx in list(vazias):
                board[idx] = atual
                vazias.remove(idx)
                seq.append(idx)

                yield from dfs(turn + 1, seq, prox)

                seq.pop()
                vazias.append(idx)
                board[idx] = '0'

        yield from dfs(0, [], primeiro)
    
    def salvar_csv(self, caminho: str, linhas: Iterable[List[str]], header: List[str]):
        with open(caminho, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(header)
            w.writerows(linhas)

    def exec(self):
        saida = "amostras.txt"
        saida_csv = 'amostras.csv'
        exit = 0
        vistos = set()
        amostras = {"Fim_de_jogo": 0, "Possibilidade_de_fim_de_jogo": 0, "Em_jogo": 0}
        limite = 83

        with open(saida, "w", encoding="utf-8") as f:
            f.write('pos1;pos2;pos3;pos4;pos5;pos6;pos7;pos8;pos9;classe\n')
            for seq, _, _ in self.gerar_partidas('1'):
                board = ['0'] * 9
                player = '1'

                for ply in range(len(seq) + 1):
                    key = "".join(board)
                    if key not in vistos:
                        vistos.add(key)
                        classe = self.classificar(board)
                        if amostras[classe] < limite:
                            f.write(self.linha_txt(board, classe) + "\n")
                            amostras[classe] += 1

                        # se já atingimos 250 de cada, paramos tudo
                        if all(v >= limite for v in amostras.values()):
                            exit = 1
                            break
                    if ply == len(seq):
                        break
                    
                    idx = seq[ply]
                    board[idx] = player
                    player = '-1' if player == '1' else '1'
                if exit == 1:
                    break
        with open(saida, "r", encoding="utf-8") as txt_file:
            reader = csv.reader(txt_file, delimiter=";")
            rows = list(reader)
        with open(saida_csv, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerows(rows)

    def vencedor_board(self, board):
        if self.check_win(board, '1'):
            return '1'
        if self.check_win(board, '-1'):
            return '-1'
        if '0' not in board:
            return 'Empate'
        return None  # não-terminal

    def exec_(self):
        saida = "amostras_250_total.txt"
        saida_csv = "amostras_.csv"
        vistos = set()

        # ------ alvo TOTAL ------
        total_alvo = 250

        # 1) Cotas por CLASSE (84+83+83 = 250)
        targets_classe = {
            "Fim_de_jogo": 84,
            "Possibilidade_de_fim_de_jogo": 83,
            "Em_jogo": 83
        }

        # 2) Subcotas em FINAIS para garantir -1 vencendo
        finais_total = targets_classe["Fim_de_jogo"]  # 84
        base = finais_total // 3                      # 28
        sobra = finais_total - base * 3               # 0 aqui (84 é múltiplo de 3)
        # Dê a sobra para '-1' se quiser reforçar ainda mais:
        targets_finais = {'1': base, '-1': base + sobra, 'Empate': base}
        cont_finais = {'1': 0, '-1': 0, 'Empate': 0}

        # 3) Cotas por POS1 (mais exemplos começando com -1)
        #    Distribuição 84/83/83 com a sobra para '-1'
        targets_pos1 = {'-1': 84, '1': 83, '0': 83}
        cont_pos1 = {'-1': 0, '1': 0, '0': 0}

        # Contadores por classe
        cont_classe = {"Fim_de_jogo": 0, "Possibilidade_de_fim_de_jogo": 0, "Em_jogo": 0}

        def terminou():
            # Para terminar, precisa bater o total E não violar as cotas
            return (sum(cont_classe.values()) >= total_alvo
                    and all(cont_classe[c] >= targets_classe[c] for c in targets_classe)
                    and all(cont_pos1[v] >= targets_pos1[v] for v in targets_pos1)
                    and all(cont_finais[r] >= targets_finais[r] for r in targets_finais))

        with open(saida, "w", encoding="utf-8") as f:
            f.write('pos1;pos2;pos3;pos4;pos5;pos6;pos7;pos8;pos9;classe\n')

            for seq, _, _ in self.gerar_partidas('1'):
                if terminou():
                    break

                board = ['0'] * 9
                player = '1'

                for ply in range(len(seq) + 1):
                    if terminou():
                        break

                    key = "".join(board)
                    if key not in vistos:
                        vistos.add(key)

                        classe = self.classificar(board)
                        p1 = board[0]  # valor da primeira posição: '1', '-1' ou '0'

                        # Checagens de cota
                        ok_classe = cont_classe[classe] < targets_classe[classe]
                        ok_pos1 = cont_pos1[p1] < targets_pos1[p1]

                        if classe == "Fim_de_jogo":
                            res = self.vencedor_board(board)  # '1' | '-1' | 'Empate'
                            ok_final = (res is not None and cont_finais[res] < targets_finais[res])
                            if ok_classe and ok_pos1 and ok_final:
                                f.write(self.linha_txt(board, classe) + "\n")
                                cont_classe[classe] += 1
                                cont_pos1[p1] += 1
                                cont_finais[res] += 1

                        else:
                            if ok_classe and ok_pos1:
                                f.write(self.linha_txt(board, classe) + "\n")
                                cont_classe[classe] += 1
                                cont_pos1[p1] += 1

                    if ply == len(seq):
                        break

                    # próxima jogada
                    idx = seq[ply]
                    board[idx] = player
                    player = '-1' if player == '1' else '1'
        with open(saida, "r", encoding="utf-8") as txt_file:
            reader = csv.reader(txt_file, delimiter=";")
            rows = list(reader)
        with open(saida_csv, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerows(rows)


    
                




