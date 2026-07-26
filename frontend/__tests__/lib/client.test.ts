/** Tests for the low-level API client: JSON handling and error mapping. */

import { apiRequest, ApiError } from "@/lib/api/client";

describe("apiRequest", () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  it("returns parsed JSON on success", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ id: 1, name: "Apollo" }),
    }) as unknown as typeof fetch;

    const result = await apiRequest<{ id: number; name: string }>("/projects");
    expect(result).toEqual({ id: 1, name: "Apollo" });
  });

  it("serialises a json body and sets the method", async () => {
    const fetchMock = jest.fn().mockResolvedValue({
      ok: true,
      status: 201,
      json: async () => ({ id: 2 }),
    });
    global.fetch = fetchMock as unknown as typeof fetch;

    await apiRequest("/projects", { method: "POST", json: { name: "X" } });

    const [, init] = fetchMock.mock.calls[0];
    expect(init.method).toBe("POST");
    expect(JSON.parse(init.body)).toEqual({ name: "X" });
  });

  it("returns undefined for 204 responses", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      status: 204,
    }) as unknown as typeof fetch;

    const result = await apiRequest<void>("/projects/1", { method: "DELETE" });
    expect(result).toBeUndefined();
  });

  it("throws ApiError carrying the backend detail on failure", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      status: 400,
      statusText: "Bad Request",
      json: async () => ({ detail: "would create a cycle" }),
    }) as unknown as typeof fetch;

    await expect(apiRequest("/cards/1/dependencies")).rejects.toMatchObject({
      name: "ApiError",
      status: 400,
      message: "would create a cycle",
    });
  });

  it("ApiError is an Error subclass", () => {
    const err = new ApiError(404, "missing");
    expect(err).toBeInstanceOf(Error);
    expect(err.status).toBe(404);
  });
});
