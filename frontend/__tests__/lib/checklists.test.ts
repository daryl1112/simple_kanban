/** Tests for the checklists API module (paths and payloads). */

import {
  addItem,
  createChecklist,
  deleteItem,
  updateItem,
} from "@/lib/api/checklists";

describe("checklists api", () => {
  let fetchMock: jest.Mock;

  beforeEach(() => {
    fetchMock = jest.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({}),
    });
    global.fetch = fetchMock as unknown as typeof fetch;
  });

  afterEach(() => jest.restoreAllMocks());

  it("createChecklist POSTs under the card", async () => {
    await createChecklist(5, { title: "QA" });
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toContain("/cards/5/checklists");
    expect(init.method).toBe("POST");
    expect(JSON.parse(init.body)).toEqual({ title: "QA" });
  });

  it("addItem POSTs under the checklist", async () => {
    await addItem(9, { text: "Write tests" });
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toContain("/checklists/9/items");
    expect(JSON.parse(init.body)).toEqual({ text: "Write tests" });
  });

  it("updateItem PATCHes the item with the toggle", async () => {
    await updateItem(12, { is_completed: true });
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toContain("/checklist-items/12");
    expect(init.method).toBe("PATCH");
    expect(JSON.parse(init.body)).toEqual({ is_completed: true });
  });

  it("deleteItem DELETEs the item", async () => {
    await deleteItem(3);
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toContain("/checklist-items/3");
    expect(init.method).toBe("DELETE");
  });
});
