package vu.thesis.mike.broadcastreceiverplugin;

import com.intellij.openapi.actionSystem.*;
import com.intellij.openapi.application.PathManager;
import com.intellij.openapi.fileEditor.FileEditorManager;
import com.intellij.openapi.fileEditor.OpenFileDescriptor;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.Messages;
import com.intellij.openapi.vfs.LocalFileSystem;
import com.intellij.openapi.vfs.VirtualFile;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.io.IOException;

public class ConfigureAction extends AnAction {
    public ConfigureAction() {
        super("Configure");
    }

    public void actionPerformed(AnActionEvent event) {
        Project project = event.getProject();

        File input = new File(PathManager.getPluginsPath() + "/BRPlugin/classes/BroadcastReceiverExerciser/configuration.json");
        File output = new File(project.getBaseDir().getPath() + "/configuration.json");

        if (!output.exists()) {
            try {
                FileUtils.copyFile(input, output);
            } catch (IOException e) {
                Messages.showMessageDialog(project, e.getMessage(), "IOException", Messages.getInformationIcon());
            }
        }

        VirtualFile file = LocalFileSystem.getInstance().refreshAndFindFileByIoFile(output);

        OpenFileDescriptor descriptor = new OpenFileDescriptor(project, file);
        FileEditorManager.getInstance(project).openTextEditor(descriptor, false);
    }
}
