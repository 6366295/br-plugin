package vu.thesis.mike.broadcastreceiverplugin;

import com.intellij.openapi.actionSystem.*;
import com.intellij.openapi.application.PathManager;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.Messages;

import java.io.IOException;

public class LaunchAction extends AnAction {
    public LaunchAction() {
        super("Launch");
    }

    // TODO: Make it work for Windows and Mac

    public void actionPerformed(AnActionEvent event) {
        Project project = event.getProject();

        StringBuilder execute = new StringBuilder();

        execute.append("gnome-terminal -x python ").
                append(PathManager.getPluginsPath()).
                append("/BRPlugin/classes/BroadcastReceiverExerciser ").
                append(project.getBaseDir().getPath()).
                append("/configuration.json ").
                append(project.getBaseDir().getPath()).
                append(" ").
                append(PathManager.getPluginsPath()).
                append("/BRPlugin/classes/BroadcastReceiverExerciser/");

        try {
            String[] args = new String[] {"bash", "-c", execute.toString()};
            new ProcessBuilder(args).start();

        } catch (IOException e) {
            Messages.showMessageDialog(project, e.getMessage(), "IOException", Messages.getInformationIcon());
        }
    }
}
