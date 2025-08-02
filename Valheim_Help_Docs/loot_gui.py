from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import yaml

# Fields expected to contain numeric values. Used for validation and casting.
NUMERIC_FIELDS = {
    "Amount",
    "AmountMin",
    "AmountMax",
    "ChanceToDrop",
    "WorldLevelMin",
    "WorldLevelMax",
    "CreatureStarsRequired",
}


class LootTableGUI:
    """Simple editor for the master loot table YAML file."""

    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.master.title("Loot Table Editor")
        self.yaml_path = Path(__file__).with_name("master_loot_table.yml")

        self.data = self._load_yaml()
        self.columns = self._collect_columns()

        self.tree = ttk.Treeview(master, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, stretch=True)
        self.tree.pack(fill=tk.BOTH, expand=True)

        for row in self.data:
            values = [row.get(col, "") for col in self.columns]
            self.tree.insert("", tk.END, values=values)

        self.tree.bind("<Double-1>", self._edit_cell)

        btn_frame = ttk.Frame(master)
        btn_frame.pack(fill=tk.X, pady=4)
        ttk.Button(btn_frame, text="Add Row", command=self._add_row).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Delete Row", command=self._delete_row).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(btn_frame, text="Save", command=self._save_data).pack(side=tk.RIGHT)

    # ------------------------------------------------------------------
    # YAML helpers
    def _load_yaml(self) -> list[dict]:
        if self.yaml_path.exists():
            with open(self.yaml_path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f) or []
            if not isinstance(content, list):
                messagebox.showerror("Error", "YAML root must be a list of rows")
                return []
            return content
        return []

    def _collect_columns(self) -> list[str]:
        cols: set[str] = set()
        for row in self.data:
            cols.update(row.keys())
        ordered = ["PrefabID", "ItemPrefab"]
        remaining = [c for c in sorted(cols) if c not in ordered]
        return ordered + remaining

    # ------------------------------------------------------------------
    # Table manipulation
    def _add_row(self) -> None:
        self.tree.insert("", tk.END, values=["" for _ in self.columns])

    def _delete_row(self) -> None:
        for item in self.tree.selection():
            self.tree.delete(item)

    def _edit_cell(self, event: tk.Event) -> None:
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        column = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
        col_index = int(column[1:]) - 1
        x, y, width, height = self.tree.bbox(row_id, column)
        value = self.tree.set(row_id, self.columns[col_index])

        entry = ttk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def commit(event: tk.Event | None = None) -> None:
            new_value = entry.get()
            col_name = self.columns[col_index]
            if col_name in NUMERIC_FIELDS and new_value.strip():
                try:
                    float(new_value)
                except ValueError:
                    messagebox.showerror(
                        "Invalid input", f"{col_name} must be numeric"
                    )
                    return
            self.tree.set(row_id, col_name, new_value)
            entry.destroy()

        entry.bind("<Return>", commit)
        entry.bind("<FocusOut>", commit)

    # ------------------------------------------------------------------
    # Save logic
    def _gather_rows(self) -> list[dict]:
        rows: list[dict] = []
        for item in self.tree.get_children():
            values = self.tree.item(item)["values"]
            row = {
                col: values[i]
                for i, col in enumerate(self.columns)
                if values[i] != ""
            }
            rows.append(row)
        return rows

    def _validate_rows(self, rows: list[dict]) -> bool:
        # Numeric validation
        for row in rows:
            for field in NUMERIC_FIELDS:
                if field in row and row[field] != "":
                    try:
                        num = float(row[field])
                        row[field] = int(num) if num.is_integer() else num
                    except ValueError:
                        messagebox.showerror(
                            "Invalid input", f"{field} must be numeric"
                        )
                        return False

        # Uniqueness validation
        seen: set[tuple] = set()
        for row in rows:
            key = (row.get("PrefabID"), row.get("ItemPrefab"))
            if None in key or "" in key:
                messagebox.showerror(
                    "Missing data", "PrefabID and ItemPrefab are required"
                )
                return False
            if key in seen:
                messagebox.showerror(
                    "Duplicate entry",
                    "Each (PrefabID, ItemPrefab) pair must be unique",
                )
                return False
            seen.add(key)
        return True

    def _save_data(self) -> None:
        rows = self._gather_rows()
        if not self._validate_rows(rows):
            return

        with open(self.yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(rows, f, sort_keys=False, allow_unicode=True)

        try:
            import generate_loot_configs

            generate_loot_configs.main()
            messagebox.showinfo("Success", "Data saved and configs generated")
        except Exception as exc:  # pragma: no cover - best effort
            messagebox.showwarning(
                "Warning", f"Saved but failed to generate configs: {exc}"
            )


def main() -> None:
    root = tk.Tk()
    LootTableGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
