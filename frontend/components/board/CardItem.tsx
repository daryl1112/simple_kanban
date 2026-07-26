"use client";

import type { DragEvent } from "react";

import type { Card, User } from "@/lib/types";

interface CardItemProps {
  card: Card;
  assignee?: User;
  onOpen: (card: Card) => void;
  onDragStart: (cardId: number) => void;
}

/**
 * A single draggable card on the board. Shows its id, title, assignee, and
 * counts of dependencies / comments. Uses native HTML5 drag-and-drop; the drag
 * payload is the card id, consumed by the destination column.
 */
export function CardItem({ card, assignee, onOpen, onDragStart }: CardItemProps) {
  function handleDragStart(e: DragEvent<HTMLDivElement>) {
    e.dataTransfer.setData("text/plain", String(card.id));
    e.dataTransfer.effectAllowed = "move";
    onDragStart(card.id);
  }

  return (
    <div
      className="card-item"
      draggable
      onDragStart={handleDragStart}
      onClick={() => onOpen(card)}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === "Enter") onOpen(card);
      }}
    >
      <div className="card-item__top">
        <span className="mono id-badge">#{card.id}</span>
        {card.dependency_ids.length > 0 && (
          <span className="mono chip" title="Dependencies">
            ⛓ {card.dependency_ids.length}
          </span>
        )}
      </div>
      <p className="card-item__title">{card.title}</p>
      <div className="card-item__meta">
        <span>{assignee ? assignee.name : "Unassigned"}</span>
        {card.comments.length > 0 && (
          <span className="mono">💬 {card.comments.length}</span>
        )}
      </div>
    </div>
  );
}
