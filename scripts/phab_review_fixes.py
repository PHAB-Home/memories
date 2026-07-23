from pathlib import Path


path = Path("src/components/viewer/Viewer.vue")
text = path.read_text()


def replace_once(old: str, new: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected exactly one match, found {count}: {old[:120]!r}")
    text = text.replace(old, new, 1)


select_block = """        {
          id: 'select',
          name: this.isSelected ? this.t('memories', 'Deselect') : this.t('memories', 'Select'),
          icon: this.isSelected ? CheckCircleIcon : CheckboxBlankCircleOutlineIcon,
          callback: this.toggleSelectCurrent,
          if: Boolean(this.timelineId && this.currentPhoto),
        },
"""
replace_once(select_block, "")
replace_once(
    """      return [
        {
          id: 'share',
""",
    """      return [
""" + select_block + """        {
          id: 'share',
""",
)

replace_once(
    """      if (!this.isOpen) {
        await utils.fragment.pop(utils.fragment.types.viewer);
        if (this.timelineId) {
          utils.bus.emit('memories:selection:sync', { timelineId: this.timelineId });
        }
        return;
      }
""",
    """      if (!this.isOpen) {
        // PhotoSwipe destroys the viewer state while route navigation is
        // awaiting. Preserve the owning timeline before yielding.
        const timelineId = this.timelineId;
        await utils.fragment.pop(utils.fragment.types.viewer);
        if (timelineId) {
          utils.bus.emit('memories:selection:sync', { timelineId });
        }
        return;
      }
""",
)

replace_once(
    """    async openDynamic(anchorPhoto: IPhoto, timeline: TimelineState) {
      this.timelineId = timeline.timelineId;
      const detail = anchorPhoto.d?.detail;
""",
    """    async openDynamic(anchorPhoto: IPhoto, timeline: TimelineState) {
      const detail = anchorPhoto.d?.detail;
""",
)
replace_once(
    """      if (!detail?.length) {
        console.error('Attempted to open viewer with no detail list!');
        return;
      }

      // Helper to compute the global anchor and count
""",
    """      if (!detail?.length) {
        console.error('Attempted to open viewer with no detail list!');
        return;
      }
      this.timelineId = timeline.timelineId;

      // Helper to compute the global anchor and count
""",
)

path.write_text(text)
