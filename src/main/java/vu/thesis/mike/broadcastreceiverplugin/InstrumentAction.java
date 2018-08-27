package vu.thesis.mike.broadcastreceiverplugin;

import com.intellij.openapi.actionSystem.*;
import com.intellij.openapi.command.WriteCommandAction;
import com.intellij.openapi.editor.Document;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.project.Project;
import com.intellij.psi.*;

public class InstrumentAction extends AnAction {
    private int cursorOffset;
    private boolean foundTiming = false;
    private boolean FoundImport = false;

    public InstrumentAction() {
        super("Instrument");
    }

    @Override
    public void update(AnActionEvent event) {

        Project project = event.getProject();
        Editor editor = event.getData(CommonDataKeys.EDITOR);

        event.getPresentation().setVisible(project != null && editor != null);
    }

    public void actionPerformed(AnActionEvent event) {
        Project project = event.getProject();

        Editor editor = event.getRequiredData(CommonDataKeys.EDITOR);
        Document document = editor.getDocument();

        // Add code at cursor location.

        cursorOffset = editor.getCaretModel().getOffset();

        WriteCommandAction.runWriteCommandAction(project, () ->
                document.insertString(cursorOffset, "timings.addSplit(\"Mandatory Split\");timings.dumpToLog();")
        );

        // Check if TimeLogger is initialized.

        PsiElement file = event.getData(LangDataKeys.PSI_FILE);

        file.accept(new JavaRecursiveElementVisitor() {
            @Override
            public void visitVariable(PsiVariable variable) {
                super.visitVariable(variable);

                if (variable.getName().equals("timings")) {
                    foundTiming = true;
                }
            }
        });

        // If not, initialize under the onReceive method.

        if (!foundTiming) {
            file.accept(new JavaRecursiveElementVisitor() {
                @Override
                public void visitMethod(PsiMethod method) {
                    super.visitMethod(method);
//                    System.out.println("Found a method at offset " + method.getTextRange().getStartOffset());
//                    System.out.println("Found a method " + method.getName());

                    if (method.getName().equals("onReceive")) {
                        int lineNum = document.getLineNumber(method.getTextOffset());
                        editor.getCaretModel().moveToOffset(document.getLineEndOffset(lineNum));
//                        System.out.println("Found a method " + lineNum);

                        cursorOffset = editor.getCaretModel().getOffset();

                        WriteCommandAction.runWriteCommandAction(project, () ->
                                document.insertString(cursorOffset, "\n        TimingLogger timings = new TimingLogger(\"MyBroadcastReceiver\", \"onReceive\");\n")
                        );
                    }
                }
            });
        }

        foundTiming = false;

        // Check if TimeLogger is imported.

        file.accept(new JavaRecursiveElementVisitor() {
            @Override
            public void visitImportStatement(PsiImportStatement is) {
                super.visitImportStatement(is);

                if (is.getText().equals("import android.util.TimingLogger;")) {
                    FoundImport = true;
                }

                int lineNum = document.getLineNumber(is.getTextOffset());
                editor.getCaretModel().moveToOffset(document.getLineEndOffset(lineNum));
            }
        });

        // If not, import it.

        if (!FoundImport) {
            cursorOffset = editor.getCaretModel().getOffset();
            WriteCommandAction.runWriteCommandAction(project, () -> document.insertString(cursorOffset, "\nimport android.util.TimingLogger;"));
        }

        FoundImport = false;
    }
}
