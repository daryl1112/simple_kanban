"use client";

import { useEffect, useState } from "react";

import { cardsApi, checklistsApi, commentsApi, dependenciesApi } from "@/lib/api";
import type { Card, User } from "@/lib/types";
import { STATUS_LABELS } from "@/lib/constants";
import { STATUS_ORDER } from "@/lib/constants";
import { Button, Markdown, Modal } from "@/components/common";
import { Checklist } from "./Checklist";

interface CardModalProps {
  card: Card;
  /** All cards in the project, for the dependency picker. */
  allCards: Card[];
  users: User[];
  onClose: () => void;
  /** Called after any mutation so the board can refresh. */
  onChanged: () => void;
}

/**
 * Detailed editor for a single card: title, Markdown description, status,
 * assignee, dependencies, checklists, and Markdown comments. Each control
 * persists via the API and then asks the parent to refresh.
 */
export function CardModal({ card, allCards, users, onClose, onChanged }: CardModalProps) {
  const [title, setTitle] = useState(card.title);
  const [description, setDescription] = useState(card.description);
  const [previewDesc, setPreviewDesc] = useState(false);
  const [newComment, setNewComment] = useState("");
  const [dependsOn, setDependsOn] = useState<number | "">("");
  const [newChecklist, setNewChecklist] = useState("");
  const [error, setError] = useState<string | null>(null);

  // Re-sync local fields if a different card is opened into the same modal.
  useEffect(() => {
    setTitle(card.title);
    setDescription(card.description);
  }, [card.id, card.title, card.description]);

  /** Run a mutation, surface errors, and refresh the board on success. */
  async function run(action: () => Promise<unknown>) {
    setError(null);
    try {
      await action();
      onChanged();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Action failed");
    }
  }

  const dependencyCards = allCards.filter((c) => card.dependency_ids.includes(c.id));
  const candidateDependencies = allCards.filter(
    (c) => c.id !== card.id && !card.dependency_ids.includes(c.id),
  );

  return (
    <Modal title={`#${card.id} · ${card.title}`} onClose={onClose}>
      {error && <p className="error-text">{error}</p>}

      <label className="field-label">Title</label>
      <input className="input" value={title} onChange={(e) => setTitle(e.target.value)} />
      <Button
        variant="ghost"
        onClick={() => run(() => cardsApi.updateCard(card.id, { title }))}
      >
        Save title
      </Button>

      <div className="field-row">
        <label className="field-label">Description (Markdown)</label>
        <button className="link-btn" onClick={() => setPreviewDesc((p) => !p)}>
          {previewDesc ? "Edit" : "Preview"}
        </button>
      </div>
      {previewDesc ? (
        <div className="preview-box">
          <Markdown>{description || "_No description_"}</Markdown>
        </div>
      ) : (
        <textarea
          className="input input--tall"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      )}
      <Button
        variant="ghost"
        onClick={() => run(() => cardsApi.updateCard(card.id, { description }))}
      >
        Save description
      </Button>

      <div className="grid-two">
        <div>
          <label className="field-label">Status</label>
          <select
            className="input"
            value={card.status}
            onChange={(e) =>
              run(() =>
                cardsApi.updateCard(card.id, {
                  status: e.target.value as Card["status"],
                }),
              )
            }
          >
            {STATUS_ORDER.map((status) => (
              <option key={status} value={status}>
                {STATUS_LABELS[status]}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="field-label">Assignee</label>
          <select
            className="input"
            value={card.assignee_id ?? ""}
            onChange={(e) =>
              run(() =>
                cardsApi.updateCard(card.id, {
                  assignee_id: e.target.value === "" ? null : Number(e.target.value),
                }),
              )
            }
          >
            <option value="">Unassigned</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <label className="field-label">Dependencies</label>
      <ul className="dep-list">
        {dependencyCards.length === 0 && <li className="muted">None</li>}
        {dependencyCards.map((dep) => (
          <li key={dep.id} className="dep-list__item">
            <span className="mono">#{dep.id}</span> {dep.title}
            <button
              className="link-btn"
              onClick={() => run(() => dependenciesApi.removeDependency(card.id, dep.id))}
            >
              remove
            </button>
          </li>
        ))}
      </ul>
      <div className="field-row">
        <select
          className="input"
          value={dependsOn}
          onChange={(e) => setDependsOn(e.target.value === "" ? "" : Number(e.target.value))}
        >
          <option value="">Select a card…</option>
          {candidateDependencies.map((c) => (
            <option key={c.id} value={c.id}>
              #{c.id} {c.title}
            </option>
          ))}
        </select>
        <Button
          variant="ghost"
          disabled={dependsOn === ""}
          onClick={() =>
            dependsOn !== "" &&
            run(async () => {
              await dependenciesApi.addDependency(card.id, dependsOn);
              setDependsOn("");
            })
          }
        >
          Add
        </Button>
      </div>

      <label className="field-label">Checklists</label>
      {card.checklists.length === 0 && <p className="muted">No checklists yet.</p>}
      {card.checklists.map((checklist) => (
        <Checklist key={checklist.id} checklist={checklist} onAction={run} />
      ))}
      <div className="field-row">
        <input
          className="input"
          placeholder="New checklist title"
          aria-label="New checklist title"
          value={newChecklist}
          onChange={(e) => setNewChecklist(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && newChecklist.trim()) {
              run(async () => {
                await checklistsApi.createChecklist(card.id, { title: newChecklist.trim() });
                setNewChecklist("");
              });
            }
          }}
        />
        <Button
          variant="ghost"
          disabled={!newChecklist.trim()}
          onClick={() =>
            run(async () => {
              await checklistsApi.createChecklist(card.id, { title: newChecklist.trim() });
              setNewChecklist("");
            })
          }
        >
          Add checklist
        </Button>
      </div>

      <label className="field-label">Comments</label>
      <ul className="comment-list">
        {card.comments.length === 0 && <li className="muted">No comments yet.</li>}
        {card.comments.map((comment) => (
          <li key={comment.id} className="comment">
            <div className="comment__body">
              <Markdown>{comment.body}</Markdown>
            </div>
            <button
              className="link-btn"
              onClick={() => run(() => commentsApi.deleteComment(comment.id))}
            >
              delete
            </button>
          </li>
        ))}
      </ul>
      <textarea
        className="input"
        placeholder="Add a comment (Markdown supported)"
        aria-label="New comment"
        value={newComment}
        onChange={(e) => setNewComment(e.target.value)}
      />
      <Button
        disabled={!newComment.trim()}
        onClick={() =>
          run(async () => {
            await commentsApi.addComment(card.id, { body: newComment });
            setNewComment("");
          })
        }
      >
        Add comment
      </Button>

      <div className="danger-zone">
        <Button
          variant="danger"
          onClick={() =>
            run(async () => {
              await cardsApi.deleteCard(card.id);
              onClose();
            })
          }
        >
          Delete card
        </Button>
      </div>
    </Modal>
  );
}
