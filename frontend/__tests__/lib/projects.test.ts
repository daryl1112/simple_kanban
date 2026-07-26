/** Tests for the projects API module (verifies paths and payloads). */

import { createProject, getBoard, listProjects } from "@/lib/api/projects";

describe("projects api", () => {
  let fetchMock: jest.Mock;

  beforeEach(() => {
    fetchMock = jest.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ([]),
    });
    global.fetch = fetchMock as unknown as typeof fetch;
  });

  afterEach(() => jest.restoreAllMocks());

  it("listProjects requests GET /projects", async () => {
    await listProjects();
    const [url] = fetchMock.mock.calls[0];
    expect(url).toContain("/projects");
  });

  it("createProject POSTs the name and description", async () => {
    fetchMock.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: 1 }),
    });
    await createProject({ name: "Apollo", description: "# Goal" });
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toContain("/projects");
    expect(init.method).toBe("POST");
    expect(JSON.parse(init.body)).toEqual({ name: "Apollo", description: "# Goal" });
  });

  it("getBoard hits the board sub-resource", async () => {
    await getBoard(7);
    const [url] = fetchMock.mock.calls[0];
    expect(url).toContain("/projects/7/board");
  });
});
