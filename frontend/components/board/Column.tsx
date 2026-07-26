"use client";

import type { DragEvent } from "react";
import { useState } from "react";

import type { BoardColumn, Card, User } from "@/lib/types";
import { STATUS_COLORS, STATUS_LABELS } from "@/lib/constants";
import { CardItem } from "./CardItem";

interface ColumnProps {
  column: BoardColumn;
  usersById: Map<number, User>;
  onOpenCard: (card: Card) => void;
  onDragStart: (cardId: number) => void;
  onDropCard: (status: BoardColumn["status"]) => void;
  onAddCard: (status: BoardColumn["status"], title: string) => void;
}

/**
 * A single status column. Acts as a drop target for cards and offers a quick
 * "add card" input at the bottom.
 */
export function Column({
  column,
  usersById,
  onOpenCard,
  onDragStart,
  onDropCard,
  onAddCard,
}: ColumnProps) {
  const [isOver, setIsOver] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const accent = STATUS_COLORS[column.status];

  function handleDrop(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsOver(false);
    onDropCard(column.status);
  }

  function handleAdd() {
    if (newTitle.trim()) {
      onAddCard(column.status, newTitle.trim());
      setNewTitle("");
    }
  }

  return (
    <section
      className={`column ${isOver ? "column--over" : ""}`}
      onDragOver={(e) => {
        e.preventDefault();
        setIsOver(true);
      }}
      onDragLeave={() => setIsOver(false)}
      onDrop={handleDrop}
    >
      <header className="column__header" style={{ borderTopColor: accent }}>
        <span className="mono column__label" style={{ color: accent }}>
          {STATUS_LABELS[column.status]}
        </span>
        <span className="mono column__count">{column.cards.length}</span>
      </header>

      <div className="column__cards">
        {column.cards.map((card) => (
          <CardItem
            key={card.id}
            card={card}
            assignee={card.assignee_id ? usersById.get(card.assignee_id) : undefined}
            onOpen={onOpenCard}
            onDragStart={onDragStart}
          />
        ))}
      </div>

      <div className="column__add">
        <input
          className="input input--sm"
          placeholder="+ Add card"
          aria-label={`Add card to ${STATUS_LABELS[column.status]}`}
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleAdd();
          }}
        />
      </div>
    </section>
  );
}
