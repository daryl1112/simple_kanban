/** Tests for the Checklist component: rendering, progress, and interactions. */

import { fireEvent, render, screen } from "@testing-library/react";

import { Checklist } from "@/components/board/Checklist";
import type { Checklist as ChecklistType } from "@/lib/types";

function buildChecklist(overrides: Partial<ChecklistType> = {}): ChecklistType {
  return {
    id: 1,
    card_id: 1,
    title: "Acceptance criteria",
    completed_count: 1,
    total_count: 2,
    created_at: "",
    updated_at: "",
    items: [
      {
        id: 10,
        checklist_id: 1,
        text: "Done thing",
        is_completed: true,
        created_at: "",
        updated_at: "",
      },
      {
        id: 11,
        checklist_id: 1,
        text: "Todo thing",
        is_completed: false,
        created_at: "",
        updated_at: "",
      },
    ],
    ...overrides,
  };
}

describe("Checklist", () => {
  it("renders the title, progress count, and items", () => {
    render(<Checklist checklist={buildChecklist()} onAction={jest.fn()} />);
    expect(screen.getByText("Acceptance criteria")).toBeInTheDocument();
    expect(screen.getByText("1/2")).toBeInTheDocument();
    expect(screen.getByText("Done thing")).toBeInTheDocument();
    expect(screen.getByText("Todo thing")).toBeInTheDocument();
  });

  it("reflects completion state in the checkboxes", () => {
    render(<Checklist checklist={buildChecklist()} onAction={jest.fn()} />);
    const boxes = screen.getAllByRole("checkbox") as HTMLInputElement[];
    expect(boxes[0].checked).toBe(true);
    expect(boxes[1].checked).toBe(false);
  });

  it("calls onAction when an item is toggled", () => {
    const onAction = jest.fn();
    render(<Checklist checklist={buildChecklist()} onAction={onAction} />);
    fireEvent.click(screen.getAllByRole("checkbox")[1]);
    expect(onAction).toHaveBeenCalledTimes(1);
    expect(typeof onAction.mock.calls[0][0]).toBe("function");
  });

  it("adds an item on Enter", () => {
    const onAction = jest.fn();
    render(<Checklist checklist={buildChecklist()} onAction={onAction} />);
    const input = screen.getByLabelText("Add an item to Acceptance criteria");
    fireEvent.change(input, { target: { value: "New item" } });
    fireEvent.keyDown(input, { key: "Enter" });
    expect(onAction).toHaveBeenCalledTimes(1);
  });

  it("does not add a blank item", () => {
    const onAction = jest.fn();
    render(<Checklist checklist={buildChecklist()} onAction={onAction} />);
    const input = screen.getByLabelText("Add an item to Acceptance criteria");
    fireEvent.keyDown(input, { key: "Enter" });
    expect(onAction).not.toHaveBeenCalled();
  });
});
