interface ChooseAnotherFileButtonProps {
  onChoose: () => void;
}

export function ChooseAnotherFileButton({ onChoose }: ChooseAnotherFileButtonProps) {
  return (
    <button className="button button--secondary" type="button" onClick={onChoose}>
      Choose another file
    </button>
  );
}