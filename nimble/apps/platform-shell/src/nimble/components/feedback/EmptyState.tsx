export function EmptyState({
  title,
  description,
}: {
  readonly title: string;
  readonly description: string;
}) {
  return (
    <section className="nimble-empty-state">
      <span aria-hidden="true">◇</span>
      <h2>{title}</h2>
      <p>{description}</p>
    </section>
  );
}
