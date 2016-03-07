import sublime, sublime_plugin
from .Packages.java_ import javapack
import re

def getImports(texts):
	packs = re.findall(r'([\A-Z][\w\.]+)', texts)
	packs += re.findall(r'([\A-Z]+[\w]+)\.', texts)
	imports = []

	for x in packs:
		result = str(javapack(x))
		if len(result) > 3:
			imports.append(result)

	imports = sorted(set(imports))
	return imports

class Easy_importCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		content = view.substr(sublime.Region(0, view.size()))
		scope = (view.scope_name(0).split(" ")[0].split(".")[1])

		if scope == "java":
			if "import " in content.lower():
				view.erase(edit, sublime.Region(0, view.size()))
				formatted = sorted(set(getImports(content)))

				previous_import = re.findall(r'import (.*);\n', content)
				final = ""
				formatted += previous_import
				formatted = sorted(set(formatted))
				for item in formatted:
					item = ("import %s;\n" % item).replace(";;", ";")
					final += item

				pattern = re.compile(r"import.*;")
				content = pattern.sub("ddd", content)
				c = content.count("ddd")
				content = (content.replace("ddd\n", "!`#~") )
				content = content.replace("!`#~" * c, final)

				# Incase of errors, just add an empty space
				content = content.replace("!`#~", "")

				view.insert(edit, 0, content)
				sublime.status_message("Easy Import: Classes Imported")
