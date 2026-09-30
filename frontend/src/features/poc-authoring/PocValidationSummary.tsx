interface PocValidationSummaryProps {
  errors: readonly string[];
}

export function PocValidationSummary({ errors }: PocValidationSummaryProps) {
  if (errors.length === 0) {
    return null;
  }

  return (
    <section className="poc-validation" role="alert" aria-labelledby="poc-validation-title">
      <h2 id="poc-validation-title">Draft response rejected</h2>
      <p>The response was not accepted as a completed POC draft.</p>
      <ul>
        {errors.map((error) => (
          <li key={error}>{error}</li>
        ))}
      </ul>
    </section>
  );
}