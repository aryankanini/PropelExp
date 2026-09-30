export interface ExtractionResult {
  pageNumber: number;
  content: string;
  confirmed: boolean;
}

export function projectReviewResults(
  results: readonly ExtractionResult[],
  failedPageNumbers: ReadonlySet<number>,
): ExtractionResult[] {
  return results.filter(
    (result) => result.confirmed || !failedPageNumbers.has(result.pageNumber),
  );
}