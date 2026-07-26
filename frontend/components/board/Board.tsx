"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { cardsApi, projectsApi, usersApi } from "@/lib/api";
import type { Board as BoardData, Card, CardStatus, User } from "@/lib/types";
import { Column } from "./Column";
import { CardModal } from "./CardModal";

interface BoardProps {
  projectId: number;
}

/**
 * The board view for a project. Owns board/user state, loads data, handles
 * drag-and-drop status moves, quick card creation, and opening the card modal.
 */
export function Board({ projectId }: BoardProps) {
  const [board, setBoard] = useState<BoardData | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [openCard, setOpenCard] = useState<Card | null>(null);
  const [error, setError] = useState<string | null>(null);
  // The id of the card currently being dragged (set on drag start).
  const draggingId = useRef<number | null>(null);

  /** Reload the board (and keep any open card in sync with fresh data). */
  const refresh = useCallback(async () => {
    try {
      const data = await projectsApi.getBoard(projectId);
      setBoard(data);
      setOpenCard((current) => {
        if (!current) return null;
        const all = data.columns.flatMap((col) => col.cards);
        return all.find((c) => c.id === current.id) ?? null;
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load board");
    }
  }, [projectId]);

  useEffect(() => {
    refresh();
    usersApi.listUsers().then(setUsers).catch(() => setUsers([]));
  }, [refresh]);

  /** Flat list of every card, used by the dependency picker in the modal. */
  const allCards = useMemo(
    () => (board ? board.columns.flatMap((col) => col.cards) : []),
    [board],
  );

  const usersById = useMemo(() => new Map(users.map((u) => [u.id, u])), [users]);

  async function handleDropCard(status: CardStatus) {
    const cardId = draggingId.current;
    draggingId.current = null;
    if (cardId == null) return;

    const card = allCards.find((c) => c.id === cardId);
    if (!card || card.status === status) return; // no-op move

    await cardsApi.updateCard(cardId, { status });
    await refresh();
  }

  async function handleAddCard(status: CardStatus, title: string) {
    await cardsApi.createCard(projectId, { title, status });
    await refresh();
  }

  if (error) return <p className="error-text">{error}</p>;
  if (!board) return <p className="empty-state">Loading board…</p>;

  return (
    <>
      <div className="board">
        {board.columns.map((column) => (
          <Column
            key={column.status}
            column={column}
            usersById={usersById}
            onOpenCard={setOpenCard}
            onDragStart={(id) => (draggingId.current = id)}
            onDropCard={handleDropCard}
            onAddCard={handleAddCard}
          />
        ))}
      </div>

      {openCard && (
        <CardModal
          card={openCard}
          allCards={allCards}
          users={users}
          onClose={() => setOpenCard(null)}
          onChanged={refresh}
        />
      )}
    </>
  );
}
