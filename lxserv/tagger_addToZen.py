# python
try:
    # Try to import zen. If Zen isn't installed, we pass.
    import zen

    # registers toolbox to the toolboxes list
    zen.Toolboxes().add('tagger', 'Tagger')

except:
    pass
