"use client";

import { useState } from "react";

import { checklistsApi } from "@/lib/api";
import type { Checklist as ChecklistType } from "@/lib/types";

interface ChecklistProps {
  checklist: ChecklistType;
  /**
   * Runs a mutation with shared error handling + board refresh. Passed down
   * from CardModal so this component stays presentational.
   */
  onAction: (action: () => Promise<unknown>) => void;
}

/**
 * A single checklist: title, a progress bar, its checkable items, an add-item
 * input, and controls to rename or delete the whole list.
 */
export function Checklist({ checklist, onAction }: ChecklistProps) {
  const [newItem, setNewItem] = useState("");
  const [renaming, setRenaming] = useState(false);
  const [title, setTitle] = useState(checklist.title);

  const { completed_count: done, total_count: total } = checklist;
  const percent = total === 0 ? 0 : Math.round((done / total) * 100);

  function addItem() {
    const text = newItem.trim();
    if (!text) return;
    onAction(async () => {
      await checklistsApi.addItem(checklist.id, { text });
      setNewItem("");
    });
  }

  return (
    <div className="checklist">
      <div className="checklist__head">
        {renaming ? (
          <input
            className="input input--sm"
            aria-label="Checklist title"
            value={title}
            autoFocus
            onChange={(e) => setTitle(e.target.value)}
            onBlur={() => {
              setRenaming(false);
              if (title.trim() && title !== checklist.title) {
                onAction(() => checklistsApi.renameChecklist(checklist.id, { title: title.trim() }));
              }
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter") (e.target as HTMLInputElement).blur();
            }}
          />
        ) : (
          <button className="checklist__title" onClick={() => setRenaming(true)}>
            {checklist.title}
          </button>
        )}
        <div className="checklist__head-right">
          <span className="mono checklist__count">
            {done}/{total}
          </span>
          <button
            className="link-btn"
            aria-label="Delete checklist"
            onClick={() => onAction(() => checklistsApi.deleteChecklist(checklist.id))}
          >
            delete
          </button>
        </div>
      </div>

      <div className="progress" role="progressbar" aria-valuenow={percent} aria-valuemin={0} aria-valuemax={100}>
        <div className="progress__fill" style={{ width: `${percent}%` }} />
      </div>

      <ul className="checklist__items">
        {checklist.items.map((item) => (
          <li key={item.id} className="checklist-item">
            <label className="checklist-item__label">
              <input
                type="checkbox"
                checked={item.is_completed}
                onChange={(e) =>
                  onAction(() =>
                    checklistsApi.updateItem(item.id, { is_completed: e.target.checked }),
                  )
                }
              />
              <span className={item.is_completed ? "checklist-item__text is-done" : "checklist-item__text"}>
                {item.text}
              </span>
            </label>
            <button
              className="link-btn"
              aria-label="Delete item"
              onClick={() => onAction(() => checklistsApi.deleteItem(item.id))}
            >
              ✕
            </button>
          </li>
        ))}
      </ul>

      <input
        className="input input--sm"
        placeholder="+ Add an item"
        aria-label={`Add an item to ${checklist.title}`}
        value={newItem}
        onChange={(e) => setNewItem(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") addItem();
        }}
      />
    </div>
  );
}
