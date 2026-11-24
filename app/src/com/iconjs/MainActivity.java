package com.iconjs;

import android.app.Activity;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.GridLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

/** Shows the icons and how to turn the pack on. */
public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle saved) {
        super.onCreate(saved);
        float dp = getResources().getDisplayMetrics().density;
        int pad = (int) (16 * dp);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(pad, pad * 3, pad, pad * 3);

        TextView head = text(18, 0xFFFE8019, true);
        head.setText("iconJS");
        root.addView(head);
        TextView how = text(12, 0xFFCBB890, false);
        how.setText(Icons.KEYS.length + " icons. To use them: Lawnchair settings > "
                + "Home screen (or General) > Icon pack > iconJS.");
        root.addView(how);

        GridLayout grid = new GridLayout(this);
        grid.setColumnCount(4);
        int cell = (getResources().getDisplayMetrics().widthPixels - 2 * pad) / 4;
        for (int n = 0; n < Icons.KEYS.length; n++) {
            LinearLayout tile = new LinearLayout(this);
            tile.setOrientation(LinearLayout.VERTICAL);
            tile.setGravity(Gravity.CENTER_HORIZONTAL);
            tile.setPadding(0, pad / 2, 0, pad / 2);
            ImageView img = new ImageView(this);
            int id = getResources().getIdentifier(Icons.KEYS[n], "drawable", getPackageName());
            if (id != 0) img.setImageResource(id);
            int size = (int) (52 * dp);
            tile.addView(img, new LinearLayout.LayoutParams(size, size));
            TextView label = text(9, 0xFF978771, false);
            label.setText(Icons.LABELS[n]);
            label.setSingleLine(true);
            label.setGravity(Gravity.CENTER);
            tile.addView(label, new LinearLayout.LayoutParams(cell, -2));
            GridLayout.LayoutParams lp = new GridLayout.LayoutParams();
            lp.width = cell;
            grid.addView(tile, lp);
        }
        root.addView(grid);

        ScrollView scroll = new ScrollView(this);
        scroll.setBackgroundColor(0xFF1E1E1E);
        scroll.addView(root);
        setContentView(scroll);
    }

    private TextView text(int sp, int color, boolean bold) {
        TextView t = new TextView(this);
        t.setTextSize(sp);
        t.setTextColor(color);
        t.setTypeface(Typeface.MONOSPACE, bold ? Typeface.BOLD : Typeface.NORMAL);
        t.setPadding(0, 0, 0, (int) (8 * getResources().getDisplayMetrics().density));
        return t;
    }
}
